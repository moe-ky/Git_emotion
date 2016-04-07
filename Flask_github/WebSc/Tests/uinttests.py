import unittest
import MainScript

apple = MainScript.Company("$AAPL")


class SimplisticTest(unittest.TestCase):

    def test(self):
        self.assertTrue(True)

    def test1(self):
        self.assertEqual(apple.data_collection(),
                         ['C:/Users/MOYIN/Desktop/Flask/WebSc/Tracker/$AAPL\\$AAPL-01-04-16.json'])

    def test2(self):
        self.assertEqual(apple.pre_process(['C:/Users/MOYIN/Desktop/Flask/WebSc/Tracker/$AAPL\\$AAPL-01-04-16.json']),
                         ['i', 'am', 'happy', 'with', 'aapl', 'today'])

    def test3(self):
        self.assertEqual(apple.emotion_analysis(["i", "am", "happy",'i', 'am', 'sad'],'Tracker\\$AAPL\\$AAPL16-03-16.json',"16-03-16",2,[]),
                          [{'contentment': 2}, {'sadness': 2}])


if __name__ == '__main__':
    unittest.main()