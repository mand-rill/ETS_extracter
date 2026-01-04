import os
import json
from pathlib import Path

def extract_ets_data(subfolder_index=3):
    # 设置ETS文件夹路径
    ets_folder = os.path.expandvars(r"%Appdata%/ETS")
    
    # 根据题号设置输出文件名
    output_file = f"extracted_data_subfolder_{subfolder_index}.json"
    
    # 存储提取的数据
    extracted_data = []
    
    try:
        # 遍历ETS文件夹
        if not os.path.exists(ets_folder):
            print(f"错误: 文件夹 {ets_folder} 不存在")
            return
        
        # 获取所有以数字命名的文件夹
        numeric_folders = []
        for item in os.listdir(ets_folder):
            item_path = os.path.join(ets_folder, item)
            if os.path.isdir(item_path) and item.isdigit():
                numeric_folders.append(item)
        
        if not numeric_folders:
            print("未找到以数字命名的文件夹")
            return
        
        print(f"找到 {len(numeric_folders)} 个以数字命名的文件夹")
        
        # 遍历每个数字文件夹
        for folder_name in numeric_folders:
            numeric_folder_path = os.path.join(ets_folder, folder_name)
            
            # 获取子目录中所有文件夹
            subfolders = []
            for sub_item in os.listdir(numeric_folder_path):
                sub_item_path = os.path.join(numeric_folder_path, sub_item)
                if os.path.isdir(sub_item_path):
                    subfolders.append(sub_item)
            
            if len(subfolders) < subfolder_index:
                print(f"文件夹 {folder_name} 中只有 {len(subfolders)} 个子文件夹，需要至少 {subfolder_index} 个，跳过")
                continue
            
            # 按字典序排序，取指定位置的子文件夹（从小到大排序）
            subfolders.sort()
            target_subfolder = subfolders[subfolder_index - 1]
            target_subfolder_path = os.path.join(numeric_folder_path, target_subfolder)
            
            # 查找content.json文件
            content_json_path = os.path.join(target_subfolder_path, "content.json")
            
            if not os.path.exists(content_json_path):
                print(f"文件夹 {folder_name} 的子文件夹 {target_subfolder} 中没有 content.json 文件")
                continue
            
            # 读取content.json文件
            try:
                with open(content_json_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # 提取ask和value字段
                if "info" in data and "question" in data["info"]:
                    for question in data["info"]["question"]:
                        extracted_item = {
                            "folder": folder_name,
                            "subfolder": target_subfolder,
                            "ask": question.get("ask", ""),
                            "values": []
                        }
                        
                        # 提取std数组中的value字段
                        if "std" in question:
                            for std_item in question["std"]:
                                extracted_item["values"].append(std_item.get("value", ""))
                        
                        extracted_data.append(extracted_item)
                
                print(f"成功处理文件夹 {folder_name}, 子文件夹 {target_subfolder}")
                
            except Exception as e:
                print(f"读取 {content_json_path} 时出错: {e}")
                continue
        
        # 将提取的数据写入输出文件
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(extracted_data, f, ensure_ascii=False, indent=2)
        
        print(f"\n提取完成! 共提取 {len(extracted_data)} 条数据")
        print(f"结果已保存到: {output_file}")
        
    except Exception as e:
        print(f"程序运行出错: {e}")

if __name__ == "__main__":
    import sys
    
    # 如果提供了命令行参数，使用参数作为题号
    if len(sys.argv) > 1:
        try:
            subfolder_index = int(sys.argv[1])
            print(f"使用自定义题号: {subfolder_index}")
        except ValueError:
            print("参数错误，使用默认题号 3")
            subfolder_index = 3
    else:
        subfolder_index = 3
        print(f"使用默认题号: {subfolder_index}")
    
    extract_ets_data(subfolder_index)
