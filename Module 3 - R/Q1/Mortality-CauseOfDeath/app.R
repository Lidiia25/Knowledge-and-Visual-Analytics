# author: Lidiia Tronina
# Data can be found here:
# https://github.com/charleyferrari/CUNY_DATA608/tree/master/module3/data

# Question 1:
#    As a researcher, you frequently compare mortality rates from particular
# causes across different States. You need a visualization that will let you see
# (for 2010 only) the crude mortality rate, across all States, from one cause
# (for example, Neoplasms, which are effectively cancers). Create a visualization
# that allows you to rank States by crude mortality for each cause of death.



library(ggplot2)
library(dplyr)
library(shiny)
library(sqldf)
library(rsconnect)
df <- read.csv("https://raw.githubusercontent.com/charleyferrari/CUNY_DATA608/master/lecture3/data/cleaned-cdc-mortality-1999-2010-2.csv", header= TRUE)

q1<-sqldf("select * from df where Year = 2010")
ui <- fluidPage(
  headerPanel('State Moratlity Rate by Cause'),
  sidebarPanel(
    selectInput('Cause', 'Cause of Death', unique(q1$ICD.Chapter),
                selected='Certain infectious and parasitic diseases')
    
  ),
  mainPanel(
    htmlOutput(outputId = 'selection'),
    plotOutput('plot1', height="auto"),
    h6("States by number of deaths for the selected cause of death.")
  )
)

server <- shinyServer(function(input, output, session) {
  
  selectedData <- reactive({
    q1 %>% filter(ICD.Chapter == input$Cause)
  })
  
  output$selection <- renderText({
    paste('<b>Death rate for: </b>', input$Cause)
  })
  
  output$plot1 <- renderPlot({
    
    ggplot(selectedData(), aes(x=reorder(State, -Crude.Rate), y=Crude.Rate)) +
      geom_col(fill = "#638DC7") +
      coord_flip() +
      geom_text(aes(label=Crude.Rate),
                size=3,
                hjust=-0.2,
                color="#3379BA") +
      xlab("State") +
      ylab("Rate") +
      theme(panel.background = element_blank())
  }, height = function() {
    session$clientData$output_plot1_width}
  )
})

shinyApp(ui = ui, server = server)
#deployApp()