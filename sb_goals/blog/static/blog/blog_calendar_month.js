$('#calendar').fullCalendar({
    defaultView: 'month',
    defaultDate: '2020-06-12',

    eventRender: function (eventObj, $el) {
        $el.popover({
            title: eventObj.title,
            content: eventObj.description,
            trigger: 'hover',
            placement: 'top',
            container: 'body'
        });
    },

    events: [{
        title: 'All Day Event',
        description: 'description for All Day Event',
        start: '2020-06-01'
    },
        {
            title: 'Long Event',
            description: 'description for Long Event',
            start: '2020-05-01',
            end: '2020-06-12'
        },
        {
            id: 999,
            title: 'Repeating Event',
            description: 'description for Repeating Event',
            start: '2020-06-09T16:00:00'
        },
        {
            id: 999,
            title: 'Repeating Event',
            description: 'description for Repeating Event',
            start: '2020-06-16T16:00:00'
        },
        {
            title: 'Conference',
            description: 'description for Conference',
            start: '2020-06-11',
            end: '2020-06-13'
        },
        {
            title: 'Meeting',
            description: 'description for Meeting',
            start: '2020-06-12T10:30:00',
            end: '2020-06-12T12:30:00'
        },
        {
            title: 'Lunch',
            description: 'description for Lunch',
            start: '2020-06-12T12:00:00'
        },
        {
            title: 'Meeting',
            description: 'description for Meeting',
            start: '2020-06-12T14:30:00'
        },
        {
            title: 'Birthday Party',
            description: 'description for Birthday Party',
            start: '2020-06-13T07:00:00'
        },
        {
            title: 'Click for Google',
            description: 'description for Click for Google',
            url: 'http://google.com/',
            start: '2020-06-28'
        }
    ]
});