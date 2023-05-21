import datetime
import json
import requests
import matplotlib.pyplot as plt

def date_to_js_timestamp(date_str):
    import datetime
    date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
    return (date - datetime.date(1970, 1, 1)).total_seconds()

def generate_data(username, start_date_input):
    today = datetime.datetime.today()
    tomorrow = today + datetime.timedelta(days=1)
    tomorrow_date = tomorrow.strftime("%Y-%m-%d")

    end_date = int(date_to_js_timestamp(tomorrow_date))
    start_date = int(date_to_js_timestamp(start_date_input))
    print(start_date)

    base_url = "https://data.typeracer.com/games?playerId=tr:" + username + "&universe=play&startDate="

    try:
        with open('data.json', 'r') as file:
            data = json.load(file)
    except:
        data = []
        while True:
            print("Entering while loop ...")
            url = base_url + str(start_date) + "&endDate=" + str(end_date)
            response = requests.get(url)
            if response.status_code == 200:
                curr_data = response.json()
                data.extend(curr_data)
                if curr_data[-1]["gn"] == 1:
                    print("completed successfully")
                    break
                end_date = int(curr_data[-1]["t"])
            else:
                break
        with open('data.json', 'w') as file:
            json.dump(data, file, indent=4)
    return data


## function calling with user_name and start_date for results
data = generate_data("leave_me_here", "2021-03-23")

print(len(data))
print(data[0])
print(type(data[0]["t"]))

# xs = [d['t']-1616457600 for d in data]
xs = [d['gn'] for d in data]
ys = [d['wpm'] for d in data]

# plt.scatter(xs, ys)
plt.plot(xs, ys)
plt.show()

# 1616457600