$(document).ready(function(){
	String.prototype.format = function() {
	    var args = arguments;
	    return this.replace(/{(\d+)}/g, function(match, number) {
		    return typeof args[number] != 'undefined'? args[number] : match })
	}
	var Arg = Backbone.Model.extend({
		defaults: { value : undefined },
		validate: function(attrs) {
		    if ((this.has('min') && (this.get('min') > this.value))||
			(this.has('max') && (this.get('max') < this.value))) {
			alert(this.get('name') + " Out of range")
			return false
		    } else return true
		}
	    });
	var ArgView = Backbone.View.extend({
		tagName : 'div',
		that : this,
		initialize : function(model, options){
		    this.options = options
		},
		events : {
		    "change .argInput" : "updateValue"
		},
		updateValue : function (event) {
		    this.model.set("value", event.currentTarget.value);
		},
		render : function() {
		    var temp = $("#argInputLine").html();
		    temp = temp.format(this.model.get("name"), this.model.get("name"), this.model.get("type"),
				       this.model.get("min"), this.model.get("max"), this.model.get('default'));
		    this.$el.html(temp)
		    return this;
		}
	    });
	var Args = Backbone.Collection.extend({model: Arg});
	var ags = undefined;
	var Task = Backbone.Model.extend({});
	var ArgsView = Backbone.View.extend({ 
		el : $("#arglistsetup"),
		//		initialize : function(options){  },
		addOne : function(model) {
		    var view = new ArgView ({ model : model });
		    this.$el.append(view.render().el);
		},
		addAll : function(){
		    var that = this;
		    ags.each(function(model){that.addOne(model);});
		},
		render : function() {
		    this.$el.html("")
		    this.addAll();
		    return this
		},
	    });
	var agsv = undefined;
        var Job = Backbone.Model.extend({
		initialize: function (model) {
		    ags = new Args(model.get('args'));
		}
	    });
	var JobView = Backbone.View.extend({
		el: "#jobsetup",
		events: {
		    "click .submit-job-btn" : "submitJob"
		},
		submitJob : function () {
		    if (ags.every(function (m) {return m.validate()})) {
			var Task = {argNames : ags.pluck('name'),
				    argVals : ags.pluck('value'),
				    funcID : this.model.get('id')};
		    }
		},
		render : function () {
		    this.$el.html("<button class=\"submit-job-btn\">Submit Job!</button>");
		    agsv = new ArgsView();
		    this.$el.prepend(agsv.render().el)
		    this.$el.show();
		}
	    });
	var FunctionListView = Backbone.View.extend({
		el: $('#functions'),
		events: {"click .functionName": "setupJob"},
		setupJob: function (event) {
		    if (agsv != undefined) { agsv = undefined;}
		    var fid = event.currentTarget.dataset.fid;
		    var func = this.model.find(function(f) {return f.get("id") == fid});
		    t = new Job(func)
		    taskView = new JobView({model:t})
		    taskView.render()
		},
		render: function (flist) {
		    var ftemps = flist.map(function(f){
			    var temp = $("#functionlist").html();
			    return temp.format(f.get("id"), f.get("name"));
			});
		    this.$el.html(ftemps);
		    this.$el.show();
		},
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
