// Some general UI pack related JS

$(function () {
    // Custom selects
    $("select").dropkick();
});

$(document).ready(function() {
    // Todo list
    $(".todo li").click(function() {
        $(this).toggleClass("todo-done");
    });

    // Init tooltips
    $("[data-toggle=tooltip]").tooltip("show");

    // Init tags input
    $("#tagsinput").tagsInput();

    // Init jQuery UI slider
    $("#slider").slider({
        min: 1,
        max: 5,
        value: 2,
        orientation: "horizontal",
        range: "min",
    });

    // JS input/textarea placeholder
    $("input, textarea").placeholder();

    // Make pagination demo work
    $(".pagination a").click(function() {
        if (!$(this).parent().hasClass("previous") && !$(this).parent().hasClass("next")) {
            $(this).parent().siblings("li").removeClass("active");
            $(this).parent().addClass("active");
        }
    });

    $(".btn-group a").click(function() {
        $(this).siblings().removeClass("active");
        $(this).addClass("active");
    });

    // Disable link click not scroll top
    $("a[href='#']").click(function() {
        return false
    });

    $(".submit").click(function(e) {
        var query = []
        $("li.todo-done").each(function() {
                        query.push($.trim($(this).text()));
                    });
        $(".submit").text('Processing...');
        $(".results").html("")
        e.preventDefault();
        $.ajax({
            url:'/',
            type:'GET',
            dataType:'json',
            data : {'query': query},
            success: function(data) {
                var resultlist = eval(data);
                for (var result in resultlist) {
                    var resultstring = "";
                    /* Single entry fields */
                    var first_name = resultlist[result]["first_name"]
                    var last_name = resultlist[result]["last_name"]
                    var headline = resultlist[result]["headline"]
                    var locality = resultlist[result]["locality"]
                    var industry = resultlist[result]["industry"]
                    
                    resultstring = '<table border="0"><tbody><tr><th>First Name</th><td>'+first_name
                    resultstring += "</td></tr><tr><th>Last Name</th><td>"+last_name
                    if (headline && headline.length>0) {
                        resultstring += "</td></tr><tr><th>Headline</th><td>"+headline
                    }
                    if (locality && locality.length>0) {
                        resultstring += "</td></tr><tr><th>Locality</th><td>"+locality
                    }
                    if (industry && industry.length>0) {
                        resultstring += "</td></tr><tr><th>Industry</th><td>"+industry+"</td></tr>"
                    }

                    /* Multiple Entry Fields */
                    var degrees = resultlist[result]["degrees"]
                    var major = resultlist[result]["major"]
                    var colleges = resultlist[result]["colleges"]
                    var job_titles = resultlist[result]["job_titles"]
                    var companies = resultlist[result]["companies"]
                    var skills = resultlist[result]["skills"]
                    var projects = resultlist[result]["projects"]

                    if (colleges && colleges.length > 0) {
                        resultstring += "<tr><th>Colleges</th><td><ul>"
                        for (var collegeindex in colleges) {
                            resultstring += "<li>"+colleges[collegeindex]+"</li>";
                        }
                        resultstring += "</ul></td></tr>"
                    }

                    if (major && major.length > 0) {
                        resultstring += "<tr><th>Majors</th><td><ul>"
                        for (var majorindex in major) {
                            resultstring += "<li>"+major[majorindex]+"</li>";
                        }
                        resultstring += "</ul></td></tr>"
                    }

                    if (degrees && degrees.length > 0) {
                        resultstring += "<tr><th>Degrees</th><td><ul>"
                        for (var degreeindex in degrees) {
                            resultstring += "<li>"+degrees[degreeindex]+"</li>";
                        }
                        resultstring += "</ul></td></tr>"
                    }

                    if (companies && companies.length > 0) {
                        resultstring += "<tr><th>Companies</th><td><ul>"
                        for (var companyindex in companies) {
                            resultstring += "<li>"+companies[companyindex]+"</li>";
                        }
                        resultstring += "</ul></td></tr>"
                    }

                    if (job_titles && job_titles.length > 0) {
                        resultstring += "<tr><th>Job Titles</th><td><ul>"
                        for (var jobindex in job_titles) {
                            resultstring += "<li>"+job_titles[jobindex]+"</li>";
                        }
                        resultstring += "</ul></td></tr>"
                    }

                    if (skills && skills.length > 0) {
                        resultstring += "<tr><th>Skills</th><td><ul>"
                        for (var skillindex in skills) {
                            resultstring += "<li>"+skills[skillindex]+"</li>";
                        }
                        resultstring += "</ul></td></tr>"
                    }

                    if (projects && projects.length > 0) {
                        resultstring += "<tr><th>Projects</th><td><ul>"
                        for (var projectindex in projects) {
                            resultstring += "<li>"+projects[projectindex]+"</li>";
                        }
                        resultstring += "</ul></td></tr>"
                    }

                    var public_profile_url = resultlist[result]["public_profile_url"]
                    resultstring += "<tr><th>Public Profile URL</th><td>"+public_profile_url+"</td></tr>"
                    resultstring += "</tbody></table><hr/>"
                    oldhtml = $(".results").html();
                    $(".results").html(oldhtml+resultstring);
                }
                $(".submit").text('Submit');
            },
            error: function(e) { 
                $(".results").text("There was some error Processing your request. Please try again");
                $(".submit").text('Submit');
            }
        });
        
    });
});