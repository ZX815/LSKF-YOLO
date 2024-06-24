import json
import xmltodict
    try:
        Name1 = "自己设置的"
        with open('接口文件修改- 英文/'  +Name1+ '.xml', 'r', encoding="UTF-16") as xml_file:
                # xml_files.append(xml_file.read())
            parsed_data = xmltodict.parse(xml_file.read())
                    # 关闭文件流，其实 不关闭with也会帮你关闭
            xml_file.close()
                    # 将字典类型转化为json格式的字符串
            json_conversion = json.dumps(parsed_data, ensure_ascii=False, indent=4)
                    # 将字符串写到文件中
            with open('Json/'+Name1+'.json', 'w', encoding="UTF-8") as json_file:
                json_file.write(json_conversion)
                json_file.close()
    except:
        print(name[i])
        with open('接口文件修改- 英文/'  +Name1+ '.xml', 'r', encoding="UTF-8") as xml_file:
                # xml_files.append(xml_file.read())
            parsed_data = xmltodict.parse(xml_file.read())
                    # 关闭文件流，其实 不关闭with也会帮你关闭
            xml_file.close()
                    # 将字典类型转化为json格式的字符串
            json_conversion = json.dumps(parsed_data, ensure_ascii=False, indent=4)
                    # 将字符串写到文件中
            with open('Json/'+Name1+'.json', 'w', encoding="UTF-8") as json_file:
                json_file.write(json_conversion)
                json_file.close()
