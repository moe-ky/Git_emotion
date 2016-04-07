import MainScript
import time

security = "$AAPL"

apple = MainScript.DataCollection(security)
apple.collect_data()

SAC = MainScript.SAC(security)
SAC.create_csv()

visual = MainScript.DataPrep(security)
visual.create_graph()
visual.correlation_csv()


