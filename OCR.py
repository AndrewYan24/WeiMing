import PDFtransform
import requests
import base64

# 继承变量
transform = PDFtransform.transform  # 转换完成状态码
pdf_page = PDFtransform.pdf_page  # pdf文件页数
pdf_name = str(PDFtransform.get_filename(PDFtransform.pdf_path))  # pdf文件名
rel_output_path = PDFtransform.rel_output_path

def fetch_token():
    api_key = 'NhNzFbapgkya4oToKvRWOH10'  # 百度智能云api key
    secret_key = 'uWt3GnGWk2VAhDGQybuISMurC4AnMGT3'  # 百度智能云secret key
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=' + api_key + '&client_secret=' + secret_key
    response = requests.get(host)
    if response:
        result = response.json()
        return result['access_token']


def read_file(image_path):
    f = open(image_path, 'rb')
    return f.read()


def ocr(token, picture_file):
    img = base64.b64encode(picture_file)
    params = {"image": img, "paragraph": "true"}
    access_token = token
    request_url = 'https://aip.baidubce.com/rest/2.0/ocr/v1/accurate' # https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    if response:
        return response.json()


if transform == 1:
    print('开始进行文字识别')
    picture_file_path = ('require/' + pdf_name + '/')
    now_page = 1
    for ocr_num in range(pdf_page):  # 按页数循环
        print('正在处理第' + str(now_page) + '页' + ' 共' + str(pdf_page) + '页')
        token = fetch_token()
        picture_file = read_file(picture_file_path + str(now_page) + '.png')
        result_json = ocr(token, picture_file)
        # 提取处理段落数
        paragraphs_result = (result_json["paragraphs_result"])
        rel_paragraphs_result = (paragraphs_result[0])
        words_result_idx = (rel_paragraphs_result["words_result_idx"])
        # 提取处理段内文字
        words_result = (result_json["words_result"])
        output_idx: int = int(max(words_result_idx))
        content = ""
        for result_idx in range(max(words_result_idx)):
            content = (content + words_result[output_idx]["words"] + "\n")
            output_idx: int = int(output_idx - 1)
            if now_page == 1:
                directory = {now_page: content}
            else:
                directory[now_page] = content
        now_page = now_page + 1
    print('文字识别完成')
    print(directory)

