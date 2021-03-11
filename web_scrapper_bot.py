activate_this = 'venv/Scripts/activate_this.py'
exec(compile(open(activate_this, "rb").read(), activate_this, 'exec'), dict(__file__=activate_this))

import os
import selenium
from selenium import webdriver
import time
from PIL import Image
import io
import requests
from selenium.common.exceptions import ElementClickInterceptedException
from tqdm import tqdm

def createDatasetDir(website_name, dataset_dir_name):
    website_dir_path = checkDir(os.getcwd() , website_name)
    print(website_dir_path)
    dataset_dir_path = checkDir(website_dir_path , dataset_dir_name)
    print(dataset_dir_path)
    return(website_dir_path, dataset_dir_path)
    
def checkDir( parent_dir_path, searching_dir):
    dir_list = os.listdir(parent_dir_path)
    if searching_dir in dir_list:
        searching_dir_path = os.path.join(parent_dir_path, searching_dir)
        return (searching_dir_path)

    else:
        searching_dir_path = os.path.join(parent_dir_path, searching_dir)
        os.mkdir(searching_dir_path)
        return (searching_dir_path)

def getImgURLs(search_url, tag):
        print('Getting Image URLS....')
        driver = webdriver.Chrome()

        driver.get(search_url)
        driver.find_element_by_class_name('btn-close').click()
        driver.find_element_by_class_name('Sk1_X').click()
        website_load_len = 0
        while( driver.execute_script('return document.body.scrollHeight') >= website_load_len ):
            driver.execute_script("window.scrollTo(0, {0});".format(website_load_len))
            time.sleep(1)
            website_load_len = website_load_len + 500

        img_urls=[]
        img_alt_names=[]
        imgs = driver.find_elements_by_tag_name(tag)
        index=0
        
        for img in imgs :
            if( img.get_attribute('src') != '' and img.get_attribute('src') != None):
                img_urls.append(img.get_attribute('src'))
                
                if ( img.get_attribute('alt') != '' ):
                    img_alt_names.append(img.get_attribute('alt'))
                else:
                    img_alt_names.append('image-{0}'.format(index) )
                    index= index+1
            else:
                continue

        driver.close()
        

        return(img_urls , img_alt_names)

def downloappendata(img_urls, img_alt_names, dir_path):
    print('Downloading {0} Images....'.format(len(img_urls))) 
    pbar = tqdm(total = len(img_urls))
    index = 1
    for url , name in zip(img_urls,img_alt_names):
        try:
            response = requests.get(url)
            img_path = os.path.join(dir_path, '{0}.jpg'.format(name))
            file = open(img_path, "wb")
        except:
            continue
        file.write(response.content)
        file.close()
        pbar.update( float("{0:.2f}".format( index/len(img_urls)*100 )) )
        index+=1

    print('Downloading Completed !!!')


if __name__ == '__main__':
    website_url = input('Enter Website URL: ') 
    tag_name = input('Enter element to extract(eg: img): ') 
    img_urls , img_names = getImgURLs(website_url, tag_name)

    website_path, dataset_path = createDatasetDir(website_url.split('.')[1] , tag_name)
    downloappendata(img_urls , img_names, dataset_path)
