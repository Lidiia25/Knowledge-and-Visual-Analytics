install.packages('rsconnect')


rsconnect::setAccountInfo(name='lidiia', token='742B3474AC1373ED65AED08F8AA69F6B', secret='RrhnERvoXFaAiHSy/Hi+BDAicqozdxNFlhWAsJok')

library(rsconnect)
rsconnect::deployApp('path/to/your/app')