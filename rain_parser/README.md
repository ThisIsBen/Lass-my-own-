# Rain Parser
This parser parses the following 3 中央氣象局 降雨機率預報 webpages every 24 hours
,and stores the parsed "時間,縣市名稱,降雨機率,溫度" data in measurement 'rain_prob'/database 'LASS_RAIN_PROB' in influxDB .

## Link

- 縣市預報 http://www.cwb.gov.tw/V7/forecast/
    - 今晚明晨 http://www.cwb.gov.tw/V7/forecast/index.htm
    - 明日白天 http://www.cwb.gov.tw/V7/forecast/index2.htm
    - 明日晚上 http://www.cwb.gov.tw/V7/forecast/index3.htm

## Target

- 時間
- 縣市名稱
- 降雨機率
- 溫度

## Format

Type: `Rain`
```json
{
  "time": "string",
  "county": "string",
  "temp": "string",
  "prob": "string"
}
```

## Execution


```
	python3 rain-parser.py

```