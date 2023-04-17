import webuiapi
import requests
import random
import json
from hashlib import md5
import time
import os 

# -*- coding: utf-8 -*-
import oss2

# 阿里云账号AccessKey拥有所有API的访问权限，风险很高。强烈建议您创建并使用RAM用户进行API访问或日常运维，请登录RAM控制台创建RAM用户。

ALIYUN_KEY_ID="Z0aTk6RgznzHAxjq"
ALIYUN_KEY_SECRET="FzPp8u8qSUr9xbeA9BGcFtXwMmlXda"
auth = oss2.Auth(ALIYUN_KEY_ID, ALIYUN_KEY_SECRET)

OSS_SAVE_DIR='http://shuchun.oss-cn-shanghai.aliyuncs.com/'


BAIDU_APP_ID = "20230411001637081"
BAIDU_APP_KEY = "fcknQ5qCPisGW1iu64Dc"
TASK_HOST = "http://101.33.74.69:5000"
TASK_GET_TASK_URI = TASK_HOST + "/api/generate_image"
SD_HOST='127.0.0.1'
SD_PORT=7860


# Endpoint以杭州为例，其它Region请按实际情况填写。
bucket = oss2.Bucket(auth, 'http://oss-cn-shanghai.aliyuncs.com', 'shuchun')

# 上传文件到OSS。
# <yourObjectName>由包含文件后缀，不包含Bucket名称组成的Object完整路径，例如abc/efg/123.jpg。
# <yourLocalFile>由本地文件路径加文件名包括后缀组成，例如/users/local/myfile.txt。
# bucket.put_object_from_file('<yourObjectName>', '<yourLocalFile>')


prompt_active_base = "(masterpiece, best quality, ultra-detailed, best shadow), (detailed background,dark fantasy), (beautiful detailed face), high contrast, (best illumination, an extremely delicate and beautiful), ((cinematic light)), colorful, hyper detail, dramatic light, intricate details, (1 lady, solo,black hair, sharp face,low twintails,red eyes, hair between eyes,dynamic angle),full body, blood splatter, swirling black light around the character, depth of field,black light particles,(broken glass),<lora:meinamix_meinaV8(05ae9ac04bd1)>"

prompt_negative = "(worst quality, low quality:1.4), monochrome, zombie,"

api = webuiapi.WebUIApi(host=SD_HOST, port=SD_PORT)



model_dict = {
    "1": {
        "name": '艺术模型',
        "desc": 'CG概念插画',
        "value": '1',
    },
    "2": {
        "name": '写真模型',
        "desc": '真人写真',
        "value": '2',
    },
    "3": {
        "name": '超漫模型',
        "desc": '高质量动漫插画',
        "value": '3',
    },
    "4": {
        "name": '动漫模型',
        "desc": '二次元风格插画',
        "value": '4',
    },
    "5": {
        "name": '彩漫模型',
        "desc": '色彩！色彩！色彩',
        "value": '5',
    },
    "6":{
        "name":'国漫',
        "desc":"国漫之光",
        "value":'6',
    },
    "7":{
        "name":"风景画",
        "desc":"风景画",
        "value":'7',
    }
}

best_promt_dict={
    "moxin":{
        "prompt_in":"shukezouma, negative space, , shuimobysim , <lora:shukezouma_v1_1:0.8>, portrait of a woman standing , willow branches, (masterpiece, best quality:1.2), traditional chinese ink painting, <lora:shuimobysimV3:0.7>, modelshoot style, peaceful, (smile), looking at viewer, wearing long hanfu, hanfu, song, willow tree in background, wuchangshuo,",
"prompt_neg":"(worst quality:2), (low quality:2), (normal quality:2), lowres, normal quality, skin spots, acnes, skin blemishes, age spot, glans, (watermark:2),",
        "url":"https://civitai.com/images/214667?modelVersionId=14856&prioritizedUserIds=454257&period=AllTime&sort=Most+Reactions&limit=20"
        
    },
    "meina":{
        "prompt_in":"upper body, 1girl, white hair, ponytail, purple eyes, (ninja), short sword, medium breats ,scarf, wallpaper, magic circle background, light particles, blue fire,",
        "prompt_neg":"(worst quality:2, low quality:2), (zombie, sketch, interlocked fingers, comic),",
        "url":"https://civitai.com/models/7240/meinamix"
    },
    "xiaorenshu":{
        "prompt_in":"upper body, 1girl, white hair, ponytail, purple eyes, (ninja), short sword, medium breats ,scarf, wallpaper, magic circle background, light particles, blue fire,",
        "prompt_neg":"(worst quality:2, low quality:2), (zombie, sketch, interlocked fingers, comic),",
        "url":"https://civitai.com/models/18323/xiaorenshu"
    },
    "iren":{
        "prompt_in":"nikon RAW photo,8 k,Fujifilm XT3,masterpiece, best quality, realistic, photorealistic,ultra detailed,extremely detailed face, solo,1girl, dudou,sitting on a window seat in a pale pink dudou, looking out at the city lights at night with a dreamy expression on her face irene1, , <lora:irene_v70:1> <lora:dudou:.5>",
        "prompt_neg":"(worst quality:2), (low quality:2), (normal quality:2), lowres, normal quality, ((monochrome)), ((grayscale)), skin spots, acnes, skin blemishes, age spot, glans,extra fingers,fewer fingers,strange fingers,bad hand,",
        "url":"https://civitai.com/models/11096/irene"
    }
}


style_dict = {
    "1": {
        "name": '',
        "value": '1',
    },
    "2": {
        "name": '帅气',
        "en": 'handsome',
        "value": '2',
    },
    "3": {
        "name": '清纯',
        "en": 'pure',
        "value": '3',
    },
    "4": {
        "name": '时尚',
        "en": 'fasion',
        "value": '4',
    },
    "5": {
        "name": '气质',
        "en": 'qualities',
        "value": '5',
    },
    "6": {
        "name": '少女',
        "en": 'maiden,puss,frail',
        "value": '6',
    },
    "7": {
        "name": 'mature',
        "value": '7',
    },
    "8": {
        "name": '荧光',
        "en": "塔罗牌",
        "value": '8',
    },
    "9": {
        "name": '塔罗牌',
        "en": "Tarot",
        "value": '9',
    },
    "10": {
        "name": '可爱',
        "en": 'cute,lovely',
        "value": '10',
    },
    "11": {
        "name": '汉服',
        "en": 'Hanfu',
        "value": '11',
    },
    "12": {
        "name": '水彩',
        "en": "watercolor",
        "value": '12',
    }
}

seed_in = -1


def fetch_task():
    resp = requests.get(TASK_GET_TASK_URI)
    tasks = resp.json()

    return tasks


def stable_diffusion_task(task_id,prompt="",width=512,height=512,steps=28,negative_prompt=prompt_negative,coefficient=1,model_id=0,style=0,batch_size=3,title="",subtitle=""):

    if width<=100:
        width=512
    if height<=100:
        width=512
        
    if steps<=5:
        steps=20
        
    prompt_latest=prompt_active_base+prompt 
    
    
    result = api.txt2img(
        enable_hr=False,
        denoising_strength=0.7,
        firstphase_width=0,
        firstphase_height=0,
        hr_scale=2,
        hr_second_pass_steps=0,
        hr_resize_x=0,
        hr_resize_y=0,
        prompt=prompt,
        styles=[],
        seed=-1,
        subseed=-1,
        subseed_strength=0.0,
        seed_resize_from_h=0,
        seed_resize_from_w=0,
        sampler_name=None,  # use this instead of sampler_index
        batch_size=batch_size,
        n_iter=1,
        steps=steps,
        cfg_scale=7.0,
        width=width,
        height=height,
        restore_faces=False,
        tiling=False,
        negative_prompt=prompt_negative,
        eta=1.0,
        s_churn=0,
        s_tmax=0,
        s_tmin=0,
        s_noise=1,
        override_settings={},
        override_settings_restore_afterwards=True,
        script_args=None,  # List of arguments for the script "script_name"
        script_name=None,
        send_images=True,
        save_images=True,
        alwayson_scripts={},
        sampler_index=None,  # deprecated: use sampler_name
        use_deprecated_controlnet=False,
    )
    save_dir="./output_images/"+str(task_id).zfill(8)
    try:
        os.mkdir(save_dir)
    except:
        print("os.mkdir("+save_dir+") failed")
    save_id=1
    print(len(result.images))
    
    saved_image_oss_paths=[]
    
    for image in result.images:
        save_path=os.path.join(save_dir,str(save_id)+".png")
        image.save(save_path)
        
        oss_save_path=os.path.join("aigc_result/",str(task_id).zfill(8),str(save_id)+".png")
        
        bucket.put_object_from_file(oss_save_path, save_path)
        saved_image_oss_paths.append(OSS_SAVE_DIR+oss_save_path)
        
        save_id=save_id+1


    return saved_image_oss_paths        



def main():
    while True:
        if True:
            tasks = fetch_task()
            print("start processing--------------------> tasks:",tasks)
            for task in tasks:
                prompt_en = task["prompt_in_en"]
                width=int(task["width"])
                height=int(task["height"])
                style=task["style"]
                model_id=task["model_id"]
                coefficient=task["coefficient"]
                step=task["step"]
                title=task["title"]
                subtitle=task["subtitle"]
                task_id=task["task_id"]
                rets=stable_diffusion_task(task_id=task_id,prompt=prompt_en,width=width,height=height,steps=step,model_id=model_id,coefficient=coefficient,title=title,)

                if rets is None:
                    continue 
                data=dict(task_id=task_id,images=rets)
                
                ret=requests.put(TASK_GET_TASK_URI,data=json.dumps(data))
                if ret.status_code==200:
                    print("task_id:",task_id," inferring succeed with results:",rets)
            
            time.sleep(3)
        
main()