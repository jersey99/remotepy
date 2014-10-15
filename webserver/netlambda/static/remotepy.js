$(document).ready(function(){
	String.prototype.format = function() {
	    var args = arguments;
	    return this.replace(/{(\d+)}/g, function(match, number) {
		    return typeof args[number] != 'undefined'? args[number] : match })
	}
	var FunctionListView = Backbone.View.extend({
		el: $('#functions'),
		events: {
		    "click .functionName": "setupTask"
		},
		setupTask: function (event) {
		    console.log(event.currentTarget.dataset.fid);
		},
		classname: "functions-list",
		render: function (flist) {
		    var that = this;
		    var ftemps = flist.map(function(f){
			    var temp = $("#functionlist").html();
			    return temp.format(f.get("id"), f.get("name"));
			});
		    this.$el.html(ftemps);
		    this.$el.show()
		},
		remove: function() {
		    this.$el.hide()
		},
	    });
	var flv = new FunctionListView();
        var Function = Backbone.Model.extend({});
	var FunctionList = Backbone.Collection.extend({
		model: Function,
		url:"/function/func",
	    });
	var fl = new FunctionList;
	fl.fetch({success:function(data){return flv.render(data)}});
    });
