$('#startTourBtn').click(function () {
  $('#introModal').modal('hide')
  introJs().setOptions({
    // disableInteraction: true,
    showBullets : true,
    showStepNumbers : true,
    tooltipClass: 'tooltipClass',
    hidePrev : true,
    skipLabel : 'Skip Tour',
    steps: [
    {
      element: document.querySelector('.step-1'),
      title: '1. Base layers',
      intro: 'List of background layers are provided to explore the study area. India States and basins boundaries which can be added as study area.',
      tooltipClass : 'step-1-tooltip',
      highlightClass : 'step-highlight',
      hidePrev : true,
      position: 'right'
    },
    
    // {
    //   element: document.querySelector('.step-2'),
    //   title: '2. Upload study area',
    //   intro: 'User can upload a spatial boundary in GeoJSON/KML formats. Note that the name of the study area will taken from the column specified in the form. If it is a multi-polygon, each polygon feature will be saved as separate area.',
    //   tooltipClass : 'step-2-tooltip',
    //   highlightClass : 'side-icons-highlight',
    //   hidePrev : false,
    //   position: 'left'
    // },
    {
      element: document.querySelector('.step-4'),
      title: '2. Add study area',
      intro: 'Add your study area from the drop down of saved list of boundaries',
      tooltipClass : 'step-4-tooltip',
      highlightClass : 'step-highlight',
      hidePrev : true,
      position: 'right'
    },

    {
      element: document.querySelector('.step-3'),
      title: '3. Digitize study area',
      intro: 'Digitize your study area boundary in the interactive map using this tool.The boundary will be saved and reuse again.',
      tooltipClass : 'step-3-tooltip',
      highlightClass : 'side-icons-highlight',
      hidePrev : false,
      position: 'left'
    },
 
    {
      element: document.querySelector('.step-6'),
      title: '4. Select Data Products ',
      intro: 'Select the Precipitation and ET product to be used in the analysis for the report.',
      tooltipClass : 'step-6-tooltip',
      highlightClass : 'step-highlight',
      hidePrev : false,
      position: 'right'
    },
    {
      element: document.querySelector('.step-5'),
      title: '5. Time Range',
      intro: 'Select the start and end year of analysis',
      tooltipClass : 'step-5-tooltip',
      highlightClass : 'step-highlight',
      hidePrev : true,
      position: 'right'
    },
    {
      element: document.querySelector('.step-7'),
      title: '7. Previous Reports',
      intro: 'View previous reports here.',
      tooltipClass : 'step-7-tooltip',
      highlightClass : 'side-icons-highlight',
      hidePrev : false,
      position: 'left'
    },
    {
      element: document.querySelector('.step-8'),
      title: 'Info',
      intro: 'Revisit this tour on the app.',
      tooltipClass : 'step-8-tooltip',
      highlightClass : 'side-icons-highlight',
      hidePrev : false,
      position: 'left'
    },
    {
      element: document.querySelector('.step-9'),
      title: 'Logout',
      intro: 'Log out from the India Water Accounting Dashboard.',
      tooltipClass : 'step-9-tooltip',
      highlightClass : 'side-icons-highlight',
      hidePrev : false,
      position: 'left'
    },
]
  }).start();  
})


