## server.R

library(dplyr)
library(shiny)
library(rsconnect)
library(ggplot2)
df <- read.csv("https://raw.githubusercontent.com/charleyferrari/CUNY_DATA608/master/lecture3/data/cleaned-cdc-mortality-1999-2010-2.csv", header= TRUE)

library(shiny)

shinyServer(function(input, output, session) {
  
  selectedData <- reactive({
    df %>% filter(ICD.Chapter == input$Cause & Year == 2010 )
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


