import pandas as pd 
train = pd.read_csv("train.csv")
test = pd.read_csv("test.csv")
#Create a data frame to store labels, another without labels, df with values only, test value df and a path variable to set location of where to store images
label_df = train['label']
mod_train = train.drop(columns= 'label')
data_values = mod_train.values
test_data_values = test.values
PATH = Path('/content/Mydrive/')
for i in range(0, len(data_values)):

    #read the correct label
    correct_label = label_df[i]

    #split the data into training and validation sets
    if np.random.rand() < 0.8:
        folder = '/train/'
        train_path = f'{PATH}' + '/train/' + str(correct_label)
        if not os.path.exists(train_path):
          os.makedirs(train_path)

    else:
        folder = '/valid/'
        valid_path = f'{PATH}' + '/valid/' + str(correct_label)
        if not os.path.exists(valid_path):
          os.makedirs(valid_path)
    
    img = data_values[i][:]

    #reshape into 28x28 pic
    img = img.reshape(28,28)

    #we need three channels into the picture
    img = np.stack((img,)*3,axis = -1)

    #change the data type to int8
    img = np.uint8(img)

    #create PIL Image
    new_img = Image.fromarray(img)

    #save the .jpg into correct folder
    new_img.save(f'{PATH}' + folder + str(correct_label) + '/' + 
    str(i) + '.jpg', 'JPEG')
for i in range(0, len(test_data_values)):

    #create test images
    folder = '/test/'
    test_path = f'{PATH}' + '/test/' 
    if not os.path.exists(test_path):
      os.makedirs(test_path)
    
    img = test_data_values[i][:]

    #reshape into 28x28 pic
    img = img.reshape(28,28)

    #we need three channels into the picture
    img = np.stack((img,)*3,axis = -1)

    #change the data type to int8
    img = np.uint8(img)

    #create PIL Image
    new_img = Image.fromarray(img)

    #save the .jpg into correct folder
    new_img.save(f'{PATH}' + folder + str(i) + '.jpg', 'JPEG')
mnist = DataBlock(
    blocks=(ImageBlock, CategoryBlock), 
    get_items=get_image_files,
    splitter = GrandparentSplitter(train_name = "train", valid_name
    = "valid"),  
    get_y=parent_label,
    item_tfms=Resize(224))

dls = mnist.dataloaders(PATH)
mnist = mnist.new(
        item_tfms = RandomResizedCrop(224, min_scale = 0.5),
        batch_tfms = aug_transforms())
dls = mnist.dataloaders(PATH,bs = 32)
learn.fit_one_cycle(2, 0.1)
#exported model predictions 
#get images to run 
folder ='/content/gdrive/My Drive/mnist/test/' 
images = get_image_files(folder)
#get model name 
name = '/mnist_model.pkl'
#load model with file/path 
modelex = str(PATH) + name
#load exported model 
learn = load_learner(modelex)
#pass in images to create test batch 
dl = learn.dls.test_dl(images)
pred_tensor, ignored, preds = learn.get_preds(dl=dl, with_decoded=True)
result = np.argmax(pred_tensor, 1)
final = pd.Series(result,name='Label')
submission=pd.concat([pd.Series(range(1,28001),name='ImageId'),final],axis=1)
submission.to_csv(str(PATH) + '/fastai-pytorch-mnist.csv',index=False)
