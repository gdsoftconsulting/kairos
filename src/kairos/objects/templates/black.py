class UserObject(dict):
    def __init__(self):
        object =    {
                        "type" : "template",
                        "id" : "BLACK",
                        "layout" : {
                                        "paper_bgcolor" : "black",
                                        "plot_bgcolor" : "black",
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
                                                        "color" : "white"                                            
                                                    }
                                    },
                        "xaxis" :   {
                                        "options" : {
                                                        "gridcolor" : "#555",
                                                    }
                                    },
                        "yaxis" :   {
                                        "options" : {
                                                        "gridcolor" : "#555",
                                                        "showline" : True,
                                                        "rangemode" : "tozero",
                                                        "anchor" : "free"
                                                    }
                                    }
                    }
        super(UserObject, self).__init__(**object)
