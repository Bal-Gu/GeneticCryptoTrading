import random


class Agent:
    def __init__(self, actions):
        self.fitting = 0
        self.candleHistory = []
        self.last_action = 0  # only -1 or 1
        self.possibleActions = random.choices([True, False], k=actions)
        self.config = dict()
        self.weight = []
        self.formatedCandles = []
        self.nextCandleClose = 0
        for i in range(actions):
            self.config[str(i)] = {"activate":False}
        for i in range(actions):
            if self.possibleActions[i]:
                self.generate_action(i,False)
        for i in range(actions):
            self.weight.append(random.uniform(-1, 1))

    def get_score(self) -> float:
        return self.fitting

    def remove_history(self):
        self.candleHistory = []
        self.last_action = 0

    def determine_action(self,candle) -> int:
        self.candleHistory.append(candle)
        results = [self.movingaverage()]
        #TODO add the other indicators

        weighted_result = 0
        for i in range(len(self.possibleActions)):
            weighted_result += self.weight[i] * results[i]
        if weighted_result < 0:
            if self.last_action == -1:
                return 0
            self.last_action = -1
            return -1
        elif weighted_result > 0:
            if self.last_action == 1:
                return 0
            self.last_action = 1
            return 1
        else:
            return 0


    def swap_action(self, i, action):
        self.config[str(i)] = action

    def swap_weight(self, i, new_weigh):
        self.config[str(i)] = new_weigh

    def cf_tf_cd(self,i):
        self.config[str(i)]["candle"] = random.choices(["High", "Low", "Close", "Open"])
        self.config[str(i)]["timeframe"] = random.choices([1, 5, 10, 30, 60, 120, 240, 480, 1440, 43200, 10080])
        self.config[str(i)]["activate"] = True

    def generate_action(self, i,mutate):
        # 0     moving average ( trendfolowing)
        # 1     exponential moving average
        # 2     Volume moving average
        # 3     Average volume line
        # 4     SAR
        # 5     moving average cross
        # 6     exponential moving average cross
        # 7     Volume moving average cross
        # 8     Average volume line cross
        # 9     MACD
        # 10    RSI
        # 11    Stochastic RSI
        # 12    Volume diff
        # 13    Bollinger Bands
        # 14    Moving flow index
        # 15    KDJ index
        # 16    On balance volume
        # 17    Commodity Channel Index
        # 18    Wm%R
        # 19    Directional Movement Index
        # 20    MTM - Momentum Index
        # 21    Ease of Movement Value
        if not mutate:
            self.cf_tf_cd(i)

        if i == 0:
            self.config["0"]["length"] = random.randint(2,500)
            self.config["0"]["previous"] = 0

        elif i == 1:
            self.config["1"]["length"] = random.randint(2,500)
            self.config["0"]["previous"] = 0

        elif i == 2:
            self.config[str(i)]["candle"] = 5 # volume index location
            self.config["2"]["previous"] = 0
        # TODO finish the other indicators.

    def get_timeframe(self, index):
        return self.config[index]["timeframe"]

    def movingaverage(self):
        if self.actions_before_act("0") < len(self.candleHistory):
            return 0
            # moving average
        previous_ma = self.config["0"]["previous"]

        ma = 0
        candle_type = self.select_candle(self.config["0"]["candle"])
        candles = self.format_candles(self.candleHistory, candle_type)
        for value in candles:
            ma += value
        current_ma = ma / len(candles)
        self.config["0"]["previous"] = current_ma
        if current_ma == 0:
            return 0
        if current_ma >= previous_ma:
            return 1
        else:
            return -1
    def moving_average_exponential(self):
        if self.actions_before_act("1") < len(self.candleHistory):
            return 0
        previous_ema = self.config["1"]["previous"]
        ema = 0
        candle_type = self.select_candle(self.config["1"]["candle"])
        candles = self.format_candles(self.candleHistory, candle_type)
        N = self.config["1"]["length"]
        for value in candles:
            k = 2 / (N+1)
            ema = (value - ema) * k + ema

        current_ema = ema
        self.config["1"]["previous"] = current_ema
        if current_ema == 0:
            return 0
        if current_ema >= previous_ema:
            return 1
        else:
            return -1
    def actions_before_act(self, index):
        if index == "0" or index == "1":
            return self.config[index]["length"] * self.config[index]["timeframe"] >= len(self.candleHistory)
        if index == "2" and len(self.candleHistory) >= 2:
            return True
        return False

    def select_candle(self, index):
        candle_type = self.config[index]["candle"]
        if str(candle_type).isdigit():
            return candle_type
        elif candle_type == "High":
            return 2
        elif candle_type == "Low":
            return 3
        elif candle_type == "Close":
            return 4
        elif candle_type == "Open":
            return 1

    def format_candles( self,candleType, candleTimeframe):
        candles = []
        window = []

        for candle in self.candleHistory:
            window.append(candle)

            if len(window) == candleTimeframe:
                if candleType == 1:
                    candles.append(window[0][1])
                elif candleType == 2:
                    candles.append(max(candle[candleType] for candle in window))
                elif candleType == 3:
                    candles.append(min(candle[candleType] for candle in window))
                elif candleType == 4:
                    candles.append(window[-1][4])
                else:
                    candles.append(sum(window[candleType]))
                window.pop(0)

        # Handle the trailing partial candle
        if len(window) > 0:
            if candleType == 1:
                candles.append(window[0][1])
            elif candleType == 2:
                candles.append(max(candle[candleType] for candle in window))
            elif candleType == 3:
                candles.append(min(candle[candleType] for candle in window))
            elif candleType == 4:
                candles.append(window[-1][4])
            else:
                candles.append(sum(candleType[candleType]))


        return candles



        