@startuml

/'class PortfolioDataForPeriod{
    +__init__(list assets, startDate, endDate)
    +list assets
    +int quantityOfAssets
    +DataFrame returns
    +DataFrame meanDailyReturns
    +DataFrame covMatrix
    +startDate
    +endDate
    +entropy
    -findBestPortfolio
}'/

class Program{
    +run()
    +init(assets, startDate, endDate)
    +Period
}


class Day{
    +List assets
    +DataFrame data
    +2Dnp.array corrMatrix
    +Float entropy
    +init(assets, day)
    -evaluateAttributes()


}

class ShannonEntropyCalculator{
    +{static}calculateEntropy(probDistribution)
}

class PlemeljSokhotski{
    +{static}calculate(corrMatrix): eigenvaluesDitribution
}

class Period{
    +List assets
    +startDate
    +endDate
    +List <Day>

}

class FileWriter{
    +{static}write(Period)
}

Day --> MyDataReader
Day --> ShannonEntropyCalculator
Day --> PlemeljSokhotski
Period --> Day
Program --> Period
Program --> FileWriter: use
@enduml