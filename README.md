# Rasa 聊天機器人

這是一個使用 Rasa 構建的聊天機器人項目，它允許您創建自定義的聊天應用程序。請注意，本文檔假定您已經在您的電腦上安裝了 Rasa 和所需的依賴項。

## 安裝

首先，確保您已經在您的 Python 環境中安裝了 Rasa。如果您尚未安裝，您可以使用以下指令進行安裝：

```bash
pip install rasa
```

然後，創建一個虛擬環境並啟動它：
'''bash
python -m venv venv
source venv/bin/activate  # 在 Windows 上，使用 `venv\Scripts\activate`
```

接下來，安裝本項目的依賴項：
```bash
pip install -r requirements.txt
```

# 訓練模型
要訓練 Rasa 機器人模型，您需要創建一個訓練數據集（這份文檔並未提供）。訓練數據集應包括對話示例、實體和意圖。

然後，使用以下命令訓練模型：
```bash
rasa train
```
然後您會得到 xxx.tar.gz 的檔案，在 models 中

模型訓練完成後，您可以使用以下指令運行機器人：
```bash
rasa run
```

# 使用機器人
機器人將運行在 http://localhost:5005（默認端口）。您可以使用任何聊天用戶界面（例如 Rasa X 或自定義界面）來與機器人互動。

# 自定義配置
您可以根據項目需求自定義 Rasa 機器人的配置。有關配置的詳細信息，請參閱 [Rasa官方文檔](https://rasa.com/docs/rasa/)。

# 版本控制
請在本項目中使用版本控制，以跟蹤代碼的變更。您可以使用 Git 等工具來管理您的項目。

# 聯絡方式
如果您有任何問題或反饋，請隨時與我們聯繫。

# 作者： Daniel
# 電子郵件：sky328423@gmail.com
