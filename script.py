import random
import requests
import json
import datetime
import argparse
import time


def get_config():
    with open("./post.json", "r", encoding='utf-8') as f:
        text = json.loads(f.read())
    config, start_time, end_time, user_agents = text["config"], text["start_time"], text["end_time"], text[
        "user_agents"]
    config["order_time"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return config, start_time, end_time, user_agents


class Reservation():
    def __init__(self, start_time, end_time, user_agent) -> None:
        self.start_time = start_time
        self.end_time = end_time
        self.user_agent = user_agent

    def post_reservation(self, config, id: int):
        url = "https://reservation.sustech.edu.cn/api/blade-app/qywx/saveOrder?userid=12232350&token=a2976e4d-fd25-4c39-a062-306349de0e7e"
        p_data = {
            "customerName": config["customer_name"],
            "customerId": "1580607610988580866",
            "customerTel": config["customer_tel"],
            "userNum": config["num_people"],
            "customerEmail": "",
            "gymId": "1297443858304540673",
            "gymName": "润杨羽毛球馆",
            "groundId": config["ground_id"][str(id)],
            "groundType": "0",
            "messagePushType": "0",
            "isIllegal": "0",
            "orderDate": config["order_time"],
            "startTime": self.start_time,
            "endTime": self.end_time,
            "tmpOrderDate": config["order_time"],
            "tmpStartTime": self.start_time,
            "tmpEndTime": self.end_time
        }
        headers = {
            "Accept": "application/json, text/plain, */*",
            "User-Agent": self.user_agent,
            # "Referer": "http://reservation.ruichengyunqin.com/clientMobile.html?code=1cVcUOBdJe8bibtLkkRVBVz3a3AT1j2LqcXrk5zglpM&state=STATE"
            "Refers": "https://reservation.sustech.edu.cn/clientMobile.html?code=W18c-zbZ4oXilWs3LFK6TXkvUZ5TqThWHbqQUAdtBRA&state=STATE"
        }
        try:
            re = requests.post(url, json=p_data, headers=headers)
            re.raise_for_status()
            re_data = json.loads(re.text)
            if re_data["success"]:
                print(str(id) + "号场地预定成功！", "时间：" + self.start_time + "  -  " + self.end_time)
                return True
            else:
                print(str(id) + "号场地预定失败! ", "时间：" + self.start_time + "  -  " + self.end_time,
                      " 原因：" + re_data["msg"])
                return False
        except requests.RequestException as e:
            print(f"请求错误: {e}")
            return False

    def post_single(self, config):
        ground_ids = list(config["ground_id"].keys())
        random.shuffle(ground_ids)
        for ground_id in ground_ids:
            time.sleep(1) # 可以根据需要更改间隔时间，为避免封号，请尽量使用较大间隔设定（>1s）
            if self.post_reservation(config, int(ground_id)):
                return


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='羽毛球场馆预定')
    parser.add_argument('re_type', type=int, help="模式选择参数: 0-固定时间模式, 1-手动回车模式")
    args = parser.parse_args()

    config, start_time, end_time, user_agents = get_config()
    random_user_agent = random.choice(user_agents)

    reservations = [Reservation(i, j, random_user_agent) for i, j in zip(start_time, end_time)]

    print("开始预定:", "固定时间模式" if args.re_type == 0 else "手动回车模式")

    # MAX_ATTEMPTS = len(start_time) * 3
    attempts = 0

    if args.re_type == 1:
        print(
            f"预定信息: customerName={config['customer_name']}, student_id={config['student_id']}, customer_tel={config['customer_tel']}")
        print("==================按一次回车，开始预定========================")
        input()
        time_difference = 0
    else:
        print(
            f"预定信息: customerName={config['customer_name']}, student_id={config['student_id']}, customer_tel={config['customer_tel']}")
        set_time = datetime.datetime.strptime(config["set_time"], "%Y-%m-%d %H:%M:%S")
        time_difference = (set_time - datetime.datetime.now()).total_seconds()

        while time_difference > 0: # 超过设定时间不予预定，此处可以根据需要更改停止条件
            if time_difference > 10:
                time.sleep(5)
            else:
                time.sleep(0.1) # 可以根据需要更改间隔时间
            time_difference = (set_time - datetime.datetime.now()).total_seconds()
            print(
                "==================距离设定时间还有: %.2f (s)========================" % (time_difference))

    # while attempts < MAX_ATTEMPTS:
    for reservation in reservations:
        reservation.post_single(config)
        attempts += 1

    print("预订结束，部分场次可能未预约成功，请手动检查。")
