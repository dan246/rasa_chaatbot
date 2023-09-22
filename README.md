# Rasa 聊天機器人

這是一個使用 Rasa 構建的聊天機器人項目，它允許您創建自定義的聊天應用程序。請注意，本文檔假定您已經在您的電腦上安裝了 Rasa 和所需的依賴項。

## 安裝

首先，確保您已經在您的 Python 環境中安裝了 Rasa。如果您尚未安裝，您可以使用以下指令進行安裝：

```bash
pip install rasa==2.6.2
pip install rasa==2.6.0
```

然後，創建一個虛擬環境並啟動它：

```bash
python -m venv venv
source venv/bin/activate  # 在 Windows 上，使用 `venv\Scripts\activate`
```

接下來，安裝本項目的依賴項：
```bash
pip install -r requirements.txt
```

# 訓練模型 & 自定義配置
要訓練 Rasa 機器人模型，您需要創建一個訓練數據集（這份文檔並未提供，可以連接 Mongodb 來轉換資料庫內的資料）。訓練數據集應包括對話示例、實體和意圖。

您可以根據項目需求自定義 Rasa 機器人的配置。有關配置的詳細信息，請參閱 [Rasa官方文檔](https://rasa.com/docs/rasa/)。

這裡將 Rasa 連接到 Mongodb 裡方便直接從資料庫裡撈取資料，資料撈出後會透由自訂義操作轉換成 nlu 接受的格式，並將其轉換成名為 question 的意圖，訓練完後可透過以下提到的指令使用，如要使用 GPT，請將您的 OPEN AI api key  貼到 actions.py 裡，
將 actions.py 修改好後，執行以下指令

```bash
rasa run actions
```
您的 data 資料夾裡應該會出現 question.yml

然後執行
```bash
rasa train --data ..\question.yml
```
這將會讓 Rasa 訓練轉換過後的 question.yml 


# 使用機器人
訓練完成後，使用以下指令執行機器人
```bash
rasa run actions
```
new cmd
```bash
rasa run -m models --enable-api --port 5002 --credentials credentials.yml
```

機器人將運行在 http://localhost:5002（默認端口）。您可以使用任何聊天用戶界面（例如 Rasa X 或自定義界面）來與機器人互動。

如要在本機端使用，請使用以下指令
```bash
rasa run actions
```
new cmd
```bash
rasa shell
```

# 與單獨使用 ChatGPT 的不同之處
當同樣的問題被連續問之後，ChatGPT 會改變自己的回答，如果發生在實驗上，可能會導致實驗步驟出錯而失敗，但 Rasa 合併 GPT-3 不會因為重複問而改變對於專業問題的回答。這是因為 ChatGPT 是基於 GPT-3 訓練的語言模型，無法保證對於重複問題的回答始終保持一致。 ChatGPT 生成的回答受其預訓練數據、上下文和隨機性的影響，可能在連續提問相同問題時產生變化。相比之下，Rasa 只是一個對話管理框架，可以與 GPT-3 或其他模型集成，但 Rasa 本身並不決定模型的行為。在 Rasa 合併 GPT-3 的配置中，Rasa 可以通過設置上下文、處理重複問題等方式來控制回答，以確保對於專業問題的回答保持一致。

# 聯絡方式
如果您有任何問題或反饋，請隨時與我們聯繫。
作者： Daniel
電子郵件：sky328423@gmail.com
