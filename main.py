import subprocess
import json
import os
import tempfile


def add_aigc_xmp_metadata(input_path, output_path, aigc_data):
    """
    为图片添加AIGC元数据字段，同时支持PNG和JPG格式
    """
    try:
        # 确保输出文件不存在
        if os.path.exists(output_path):
            os.remove(output_path)

        # 判断文件格式
        is_png = input_path.lower().endswith('.png')

        # 创建临时exiftool配置文件，根据格式选择配置
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            if is_png:
                # PNG配置（保留原有效配置）
                f.write('''%Image::ExifTool::UserDefined = (
                    'Image::ExifTool::PNG::TextualData' => {
                        AIGC => {
                            Name => 'AIGC',
                            Writable => 'string',
                        },
                    },
                    'Image::ExifTool::XMP::Main' => {
                        AIGC => {
                            Name => 'AIGC',
                            Writable => 'string',
                        },
                    },
                );
                1;''')
            else:
                # JPG专用配置（针对XMP区块优化）
                f.write('''%Image::ExifTool::UserDefined = (
                    'Image::ExifTool::XMP::dc' => {
                        AIGC => {
                            Name => 'AIGC',
                            Writable => 'string',
                            Group => 'XMP-dc',
                        },
                    },
                );
                1;''')
            config_path = f.name

        # 转换AIGC数据为JSON，并对引号进行转义
        aigc_json = json.dumps(aigc_data, ensure_ascii=False, separators=(',', ':'))
        aigc_json_escaped = aigc_json.replace('"', '\\"')

        # 构建命令：根据格式选择参数
        if is_png:
            command = (
                f'exiftool -config "{config_path}" '
                f'-PNG:AIGC="{aigc_json_escaped}" '
                f'-XMP:AIGC="{aigc_json_escaped}" '
                f'-o "{output_path}" "{input_path}"'
            )
        else:
            # JPG专用命令，使用dc命名空间确保兼容性
            command = (
                f'exiftool -config "{config_path}" '
                f'-XMP-dc:AIGC="{aigc_json_escaped}" '
                f'-o "{output_path}" "{input_path}"'
            )

        # 执行命令
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            check=True
        )

        # 清理临时配置文件
        os.unlink(config_path)

        print(f"成功添加AIGC字段到 {output_path}")
        print(f"验证命令: exiftool {output_path}")

    except subprocess.CalledProcessError as e:
        print(f"exiftool执行错误: {e.stderr}")
    except Exception as e:
        print(f"处理出错: {str(e)}")


if __name__ == "__main__":
    aigc_info = {
        "Label": "1",
        "ContentProducer": "00000000000000000000000000000",
        "ProduceID": "33aAROBAQOOK4K6FXe9TNg",
        "ReservedCode1": "LBkc9peJ0GoxPECtYBct7vfZZgZvwy4FZrhe/DJovt3rGFEyBJ4z5WZYsl9yWMbLRQK0uAqSXor5oKgFgp5hSWIBkg6R9P/aw7r7gDSiddVA6Mme7AXYWARwbjIpdmaSGyZrlQWZDchs7M+aKfM9k1Wz+b+KFQt4th+6LpH3Xrf371m6yzYXJp8LFXsjC5c4xjPn9yiVh9KsGALv9ZivDxcaEp+fjj+kLWDV+iJRVqvLXlX/gVAuu2Vv9nrsOnUe5aAEKYomGZhTTMqKdtW7yw==",
        "ContentPropagator": "00000000000000000000000000000",
        "PropagateID": "33aAROBAQOOK4K6FXe9TNg",
        "ReservedCode2": "LBkc9peJ0GoxPECtYBct7vfZZgZvwy4FZrhe/DJovt3rGFEyBJ4z5WZYsl9yWMbLRQK0uAqSXor5oKgFgp5hSWIBkg6R9P/aw7r7gDSiddVA6Mme7AXYWARwbjIpdmaSGyZrlQWZDchs7M+aKfM9k1Wz+b+KFQt4th+6LpH3Xrf371m6yzYXJp8LFXsjC5c4xjPn9yiVh9KsGALv9ZivDxcaEp+fjj+kLWDV+iJRVqvLXlX/gVAuu2Vv9nrsOnUe5aAEKYomGZhTTMqKdtW7yw=="
    }

    # 处理JPG
    add_aigc_xmp_metadata("3.PNG", "3_.PNG", aigc_info)
