from difflib import SequenceMatcher

def similarity_score(str1, str2):
    return SequenceMatcher(None, str1, str2).ratio()

def check_rfid_plate(rfid_id, license_plate, file_path, threshold=0.6):
    try:
        with open(file_path, "r") as file:
            lines = file.readlines()

            for line in lines:

                data_id, data_plate = line.strip().split(":")
                data_id = data_id.strip()
                data_plate = data_plate.strip()


                if rfid_id.strip() == data_id:

                    score = similarity_score(license_plate.strip(), data_plate)
                    if score >= threshold:
                        return 1

        return 0
    except FileNotFoundError:
        print(f"File {file_path} không tồn tại.")
        return 0
    except Exception as e:
        print(f"Lỗi xảy ra: {e}")
        return 0


