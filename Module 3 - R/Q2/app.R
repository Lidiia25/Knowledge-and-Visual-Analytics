# Data can be found here:
# https://github.com/charleyferrari/CUNY_DATA608/tree/master/module3/data

# Question 2:
#    Often you are asked whether particular States are improving their mortality
# rates (per cause) faster than, or slower than, the national average. Create a
# visualization that lets your clients see this for themselves for one cause of
# death at the time. Keep in mind that the national average should be weighted by
# the national population.


library(ggplot2)
library(dplyr)
library(plotly)
library(shiny)

URL <- 'https://raw.githubusercontent.com/charleyferrari/CUNY_DATA608/master/lecture3/data/cleaned-cdc-mortality-1999-2010-2.csv'
df <- read.csv(URL)

national <- df %>%
  group_by(ICD.Chapter, Year) %>%
  summarize(Crude.Rate = round((sum(Deaths) / sum(Population)) * 100000, 2)) %>%
  mutate(State = "National") %>%
  arrange(Year) %>%
  tbl_df()

state <- df %>%
  select(ICD.Chapter, Year, State, Crude.Rate)%>%
  tbl_df()

ui <- fluidPage(
  headerPanel('State Mortality Rates Explorer'),
  sidebarPanel(
    selectInput('Cause', 'Cause of Death', unique(state$ICD.Chapter),
                selected='Certain infectious and parasitic diseases'),
    selectizeInput('State', 'Select up to 5 states to compare with the national average',
                   unique(df$State), selected='NY', options = list(maxItems = 5))
  ),
  mainPanel(
    htmlOutput(outputId = 'Title'),
    plotlyOutput('plot1'),
    h6("Number of deaths per 100,000 people")
  )
)

server <- function(input, output) {
  
  output$Title <- renderText({
    paste('<b>Death rate for: </b>', input$Cause)
  })
  
  nationalData <- reactive({
    national %>%
      filter(ICD.Chapter == input$Cause)
  })
  
  stateData <- reactive({
    state %>%
      filter(ICD.Chapter == input$Cause & State %in% input$State)
  })
  
  combined <- reactive({
    merge(x = nationalData(), y = stateData(), all = TRUE)
  })
  
  output$plot1 <- renderPlotly({
    
    plot_ly(combined(), x = ~Year, y = ~Crude.Rate, color = ~State, type='scatter',
            mode = 'lines', line = list(width = 4)) %>%
      layout(xaxis = list(title = ""),
             yaxis = list(side = 'left',
                          showgrid = FALSE,
                          zeroline = FALSE))
  })
  
}

shinyApp(ui = ui, server = server)