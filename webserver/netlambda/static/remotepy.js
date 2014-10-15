$(document).ready(function(){
	String.prototype.format = function() {
	    var args = arguments;
	    return this.replace(/{(\d+)}/g, function(match, number) {
		    return typeof args[number] != 'undefined'? args[number] : match })
	}
        var Task = Backbone.Model.extend({
		initialize: function () {
		    
		}
	    });
	var FunctionListView = Backbone.View.extend({
		el: $('#functions'),
		events: {"click .functionName": "setupTask"},
		setupTask: function (event) {
		    var fid = event.currentTarget.dataset.fid;
		    var m = this.model.model.find(function(f) {return f.get("id") == fid});
		    t = new Task({})
		},
		classname: "functions-list",
		render: function (flist) {
		    var ftemps = flist.map(function(f){
			    var temp = $("#functionlist").html();
			    return temp.format(f.get("id"), f.get("name"));
			});
		    this.$el.html(ftemps);
		    this.$el.show();
		},
		initialize: function(model) {this.model = model},
		remove: function() {
		    this.$el.hide()
		},
	    });
        var Function = Backbone.Model.extend({});
	var FunctionList = Backbone.Collection.extend({
		model: Function,
		url:"/function/func",
	    });
	var fl = new FunctionList;
	var flv = new FunctionListView({model:fl});
	fl.fetch({success:function(data){return flv.render(data)}});
    });
