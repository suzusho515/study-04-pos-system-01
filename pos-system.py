import csv
import datetime

CSVPATH = "./master.csv"

dt_now = datetime.datetime.now()
file_name = "./" + dt_now.strftime('%Y-%m-%d-%H-%M-%S') + ".csv"

### 商品クラス
class Item:
    def __init__(self,item_code,item_name,price):
        self.item_code=item_code
        self.item_name=item_name
        self.price=price
    
    def get_price(self):
        return self.price

### オーダークラス
class Order:
    def __init__(self,item_master):
        self.item_code_list=[]
        self.item_name_list=[]
        self.item_price_list=[]
        self.item_count_list = []
        self.item_total_amount_list=[]
        self.item_master=item_master
    
    def add_item_order(self,item_code,item_name,item_value,item_count,total_amount):
        self.item_code_list.append(item_code)
        self.item_name_list.append(item_name)
        self.item_price_list.append(item_value)
        self.item_count_list.append(item_count)
        self.item_total_amount_list.append(total_amount)
    
    def view_item_list(self):
        f = open(file_name, 'a', encoding="utf-8_sig")
        
        for code,name,price,count,total_amount in \
            zip(self.item_code_list,self.item_name_list,self.item_price_list,self.item_count_list,self.item_total_amount_list):
            #結果表示
            print(f"商品コード:{code} 商品名:{name} 価格:{price} 個数:{count} 商品金額{total_amount}")
            #textfileへの書き込み
            f.write(f"商品コード:{code} 商品名:{name} 価格:{price} 個数:{count} 商品金額{total_amount}\n")  
        
        #合計金額と合計個数の計算
        self.result_total_amount = sum(self.item_total_amount_list)
        self.item_count_list = [int(i) for i in self.item_count_list] #int型に変換
        self.result_total_price = sum(self.item_count_list)

        print(f"合計金額は{self.result_total_amount}で、合計個数は{self.result_total_price}です")
        #textfileへの書き込み
        f.write(f"合計金額は{self.result_total_amount}で、合計個数は{self.result_total_price}です\n")  
        f.close()

    def return_name_value(self):
        while True:    
            input_code = input("商品コードを入力してください (終了する場合999を入力)>>> ")
            if input_code != "999":
                input_count = input("個数を入力してください>>> ")    
                for rist in self.item_master:
                    if input_code == rist.item_code:
                        total_amount = self.total_amount_calculation(rist.price, input_count)
                        self.add_item_order(rist.item_code, rist.item_name, rist.price, input_count, total_amount)          
            elif input_code == "999": #終了コード999
                print("登録終了")
                break

    def total_amount_calculation(self, price, input_count):
        total_amount = int(price) * int(input_count)
        return total_amount

    def change_money(self):
        f = open(file_name, 'a', encoding="utf-8_sig")
        
        while True:    
            input_money = input("お預かり金額の入力>>> ") 
            result_change_money = int(input_money) - self.result_total_amount
            if result_change_money > 0:
                print(f"おつりは{result_change_money}円です")
                #textfileへの書き込み
                f.write(f"おつりは{result_change_money}円です") 
                f.close()
                break
            elif result_change_money == 0:
                print("おつりはありません")
                #textfileへの書き込み
                f.write("おつりはありません")
                f.close()
                break
            elif result_change_money < 0:
                print("お預かり金額が不足しています")
                #textfileへの書き込み
                f.write("お預かり金額が不足しています\n")  
        
def get_item_csv(CSVPATH):
    # CSVからアイテムの読込
    item_code_temp=[]
    item_name_temp=[]
    item_value_temp=[]
    f = open(CSVPATH, 'r' , encoding="utf-8_sig")
    reader = csv.reader(f)
    for row in reader:
        item_code_temp.append(row[0])
        item_name_temp.append(row[1])
        item_value_temp.append(row[2])
        
    f.close()

    #ヘッダー削除
    del item_code_temp[0]
    del item_name_temp[0]
    del item_value_temp[0]

    #マスターへ登録
    return create_master(item_code_temp,item_name_temp,item_value_temp)
    
def create_master(item_code_temp,item_name_temp,item_value_temp):
    item_master=[]
    for code,name,value in zip(item_code_temp,item_name_temp,item_value_temp):        
        item_master.append(Item(code,name,value))
    return item_master

### メイン処理
def main():
    
    #CSVからアイテム情報を取得
    item_master = get_item_csv(CSVPATH)

    # オーダー登録
    order = Order(item_master)

    #商品名と価格の取得
    order.return_name_value()
   
    # オーダー表示
    order.view_item_list()

    #お預かり金額とおつり取得
    order.change_money()
    
if __name__ == "__main__":
    main()