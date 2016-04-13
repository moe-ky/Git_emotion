import unittest
import MainScript


class SimplisticTest(unittest.TestCase):

    def test(self):
        self.assertTrue(True)

    def test1(self):
        self.assertEqual(MainScript.DataCollection("$AAPL").collect_data(),
                         ['C:/Users/MOYIN/Desktop/Flask/WebSc/Tracker/$AAPL\\$AAPL-01-04-16.json'])

    def test2(self):
        self.assertEqual(MainScript.PreProcess("$AAPL",
                                               ['C:/Users/MOYIN/Desktop/Flask/WebSc/Tracker/$AAPL\\$AAPL-01-04-16.json']
                                               ).pre_process(),
                         ['i', 'am', 'happy', 'with', 'aapl', 'today'])

    def test3(self):
        self.assertEqual(MainScript.EAC("$AAPL",["i", "am", "happy",'i', 'am', 'sad'],
                                        'Tracker\\$AAPL\\$AAPL16-03-16.json',"16-03-16",2,[]).emotion_analysis(),
                          [{'contentment': 2}, {'sadness': 2}])

    def test4(self):
        self.assertEqual(MainScript.SAC("$AAPL").create_csv(),
                         "C:/Users/MOYIN/Desktop/Flask/WebSc/result/$AAPL/Csv_data/$AAPL.csv")

    def test5(self):
        self.assertEqual(MainScript.DataPrep("$AAPL").create_graph(),True)
        self.assertEqual(MainScript.DataPrep("$AAPL").correlation_csv(),
                         "C:/Users/MOYIN/Desktop/Flask/static/Companies/$AAPL/$AAPL_CT.csv")
if __name__ == '__main__':
    unittest.main()