import webuiapi

prompt_active = "(masterpiece, best quality, ultra-detailed, best shadow), (detailed background,dark fantasy), (beautiful detailed face), high contrast, (best illumination, an extremely delicate and beautiful), ((cinematic light)), colorful, hyper detail, dramatic light, intricate details, (1 lady, solo,black hair, sharp face,low twintails,red eyes, hair between eyes,dynamic angle),full body, blood splatter, swirling black light around the character, depth of field,black light particles,(broken glass),magic circle,<lora:meinamix_meinaV8(05ae9ac04bd1)>"

prompt_negative = "(worst quality, low quality:1.4), monochrome, zombie,"

BAIDU_APP_ID="20230411001637081"
BAIDU_APP_KEY="fcknQ5qCPisGW1iu64Dc"

api = webuiapi.WebUIApi(host='127.0.0.1', port=7860)



import requests
import random
import json
from hashlib import md5

class BaiduFanyi:
    def __init__(self, appid, appkey):
        self.appid = appid
        self.appkey = appkey
        endpoint = 'https://api.fanyi.baidu.com'
        path = '/api/trans/vip/translate'
        self.url = endpoint + path

    def _make_md5(self, s, encoding='utf-8'):
        return md5(s.encode(encoding)).hexdigest()

    def translate(self, text, fromLang="zh", toLang="en"):
        query = text
        salt = random.randint(32768, 65536)
        sign = self._make_md5(self.appid + query
                              + str(salt) + self.appkey)

        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        payload = {'appid': self.appid, 'q': query, 'from': fromLang,
                   'to': toLang, 'salt': salt, 'sign': sign}

        r = requests.post(self.url, params=payload, headers=headers)
        result_json = json.loads(r.text)
        result_list = []

        if 'error_code' in result_json:
            return result_json['error_msg']
        else:
            for result in result_json["trans_result"]:
                result_list.append(result['dst'])
            return "\n".join(result_list)


translater=BaiduFanyi(appid=BAIDU_APP_ID,appkey=BAIDU_APP_KEY)

seed_in = -1

result = api.txt2img(
    enable_hr=False,
    denoising_strength=0.7,
    firstphase_width=0,
    firstphase_height=0,
    hr_scale=2,
    hr_second_pass_steps=0,
    hr_resize_x=0,
    hr_resize_y=0,
    prompt=prompt_active,
    styles=[],
    seed=-1,
    subseed=-1,
    subseed_strength=0.0,
    seed_resize_from_h=0,
    seed_resize_from_w=0,
    sampler_name=None,  # use this instead of sampler_index
    batch_size=1,
    n_iter=1,
    steps=None,
    cfg_scale=7.0,
    width=512,
    height=512,
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
    save_images=False,
    alwayson_scripts={},
    sampler_index=None,  # deprecated: use sampler_name
    use_deprecated_controlnet=False,
)

print(result.images)