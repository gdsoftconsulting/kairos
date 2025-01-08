class UserObject(dict):
    def __init__(self):
        object =    {
                        "type" : "template",
                        "id" : "DEFAULT",
                        "layout" : {
                                        "paper_bgcolor" : "white",
                                        "plot_bgcolor" : "white",
                                        "legend" :  {
                                                        "tracegroupgap" : 0,
                                                        "borderwidth" : 1
                                                    },
                                        "hovermode" : "closest",
                                        "title" :   {
                                                        "x" : 0.5,
                                                        "xanchor" : "center",
                                                    },
                                        "font" :    {
                                                        "color" : "black"
                                                    }
                                    },
                        "xaxis" :   {
                                        "options" : {
                                                        "gridcolor" : "#eee",
                                                    }
                                    },
                        "yaxis" :   {
                                        "options" : {
                                                        "gridcolor" : "#eee",
                                                        "showline" : True,
                                                        "rangemode" : "tozero",
                                                        "anchor" : "free"
                                                    }
                                    }
                    }
        super(UserObject, self).__init__(**object)
