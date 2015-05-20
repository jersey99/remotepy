$(document).ready(function(){
	String.prototype.format = function() {
	    var args = arguments;
	    return this.replace(/{(\d+)}/g, function(match, number) {
		    return typeof args[number] != 'undefined'? args[number] : match })
	}
	var Arg = Backbone.Model.extend({
		defaults: { value : undefined },
		initialize: function() {
		    this.set("value",this.get('default'));
		    _.bindAll(this,"validate");
		},
		validate: function(attrs) {
		    if ((this.has('min') && (this.get('min') > this.value))||
			(this.has('max') && (this.get('max') < this.value))) {
			alert(this.get('name') + " Out of range")
			return false
		    } else return true
		}
	    });
	var ArgView = Backbone.View.extend({
		tagName : 'tr',
		initialize : function(model, options){
		    this.options = options
		},
		events : {
		    "change .argInput" : "updateValue"
		},
		updateValue : function (event) {
		    var v = _.map(this.model.get("desc_list"), function (x) { return x === event.currentTarget.value ? 1: 0; });
		    this.model.set("value", v);
		},
		render : function() {
		    var m = this.model;
		    if (m.get("meta_type") != null) {
			var y = "<td><b>" + m.get("name") + "</b></td><td></td><td></td><td>";
			yy = _.map(_.zip(m.get("desc_list"), eval(m.get("default"))),
				   function (x) {
				       var checked = function (x) {return (x===1) ? "checked=\"checked\"" : "";};
				       return $("#argInputMeta").html().format(m.get("name"),x[0],checked(x[1]),m.get("meta_type"));
				   });
			this.$el.append(y + yy.join(' ') + "</td><td> [" +m.get("comment") + "]</td>");
		    } else {
			this.$el.append($("#argInputLine").html().format(m.get("name"), m.get("type"),
								       m.get("min"), m.get("max"),
								       m.get('default'), m.get("comment")));
		    }
		    return this;
		}
	    });
	var Args = Backbone.Collection.extend({ model: Arg });
	var ags = undefined;
	var ArgsView = Backbone.View.extend({
		el : $("#arglistsetup"),
		addOne : function(model) {
		    var view = new ArgView ({ model : model });
		    this.$el.append(view.render().el);
		},
		addAll : function(){
		    var that = this;
		    ags.each(function(model){that.addOne(model);});
		},
		render : function() {
		    this.$el.html("");
		    this.$el.html("<tr><td>Arg-Name</td> <td>Type</td> <td>Element Range</td> <td>Input w/ Default</td> <td>Description</td></tr>")
		    this.addAll();
		    return this
		},
		close : function() {
		    this.remove();
		    this.unbind();
		}
	    });
	var agsv = undefined;
        var Job = Backbone.Model.extend({
		initialize: function () {ags = new Args(this.get('args'));}
	    });
	var Task = Backbone.Model.extend({urlRoot: '/task/t'});
	var TaskView = Backbone.View.extend({
		el : "#jobresult",
		timeoutID : undefined,
		timeoutVal : 500,
		initialize : function() {
		    this.model.bind('change:completed', this.render, this);
		    _.bindAll(this, 'render', "close");
		},
		close : function() {
		    this.model.unbind('change:completed', this.render);
		    this.$el.empty();
		    this.undelegateEvents();
		},
		render : function () {
		    var temp = $('#jobResultLine').html();
		    var args = _.map(_.zip(this.model.get('argNames'),this.model.get('argVals')),
				     function(arg){return arg[0]+'='+arg[1]}).join(', ');
		    if (this.model.get('completed')) {
			temp = temp.format(this.model.get('name'),args,this.model.get('retVal'));
			if (this.timeoutID != undefined) {
			    clearInterval(this.timeoutID);
			}
		    } else {
			temp = temp.format(this.model.get('name'),args," Computing ...");
			var that = this;
			if (this.timeoutID != undefined) clearInterval(this.timeoutID);
			this.timeoutID = setInterval(function(){that.model.fetch();},this.timeoutVal);
			this.timeoutVal = this.timeoutVal * 2;
		    }
		    this.$el.html(temp);
		}
	    });
	var JobView = Backbone.View.extend({
		el: "#jobsetup",
		initialize: function() {
		    _.bindAll(this,"submitJob", "render", "close");
		},
		events: {"click .minimal" : "submitJob"},
		tv : undefined,
		submitJob : function () {
		    if (ags.every(function (m) {return m.validate()})) {
			var t = new Task({argNames : ags.pluck('name'),
					  argVals : ags.pluck('value'),
					  function: { id: this.model.get('id'),
						      name: this.model.get('name')}});
			var that = this;
			t.save(null,{success:function(model, response){
				    that.tv = new TaskView({model:model});
				    that.tv.render();
				}});
		    }
		},
		render : function () {
		    this.$el.html($("#minimal-button").html());
		    agsv = new ArgsView();
		    this.$el.prepend(agsv.render().el)
		    this.$el.show();
		},
		close: function() {
		    if (this.tv != undefined) this.tv.close();
		    this.undelegateEvents();
		    this.$el.hide();
		}
	    });
	var FunctionListView = Backbone.View.extend({
		el: $('#functions'),
		initialize: function() {_.bindAll(this,"setupJob","render","close")},
		events: {"click .functionName": "setupJob"},
		jv: undefined,
		setupJob: function (event) {
		    if (agsv != undefined) { agsv.close(); agsv = undefined;}
		    var fid = event.currentTarget.dataset.fid;
		    var func = this.model.find(function(f) {return f.get("id") == fid});
		    var t = new Job(func.toJSON());
		    if (this.jv != undefined) {this.jv.close();}
		    this.jv = new JobView({model:t});
		    this.jv.render();
		},
		render: function () {
		    var ftemps = this.model.map(function(f){
			    var temp = $("#functionlist").html();
			    return temp.format(f.get("id"), f.get("name"));
			});
		    this.$el.html(ftemps);
		    this.$el.show();
		},
		close : function () {
		    if (this.jv != undefined) this.jv.close();
		    this.undelegateEvents();
		    this.$el.hide();
		}
	    });
        var Function = Backbone.Model.extend({});
	var FunctionList = Backbone.Collection.extend({
		model: Function,
		url:"/function/func",
	    });

	var Package = Backbone.Model.extend({});
	var PackageList = Backbone.Collection.extend({
		model: Package,
		url: "/package/pack",
	    });
	var PackageListView = Backbone.View.extend({
		el: $('#packages'),
		initialize: function() {_.bindAll(this,"viewFunctionList","render")},
		events: {"click .packageName": "viewFunctionList"},
		flv: undefined,
		viewFunctionList: function (event) {
		    if (this.flv != undefined) {this.flv.close();}
		    var pid = event.currentTarget.dataset.pid;
		    var pack = this.model.find(function(p) {return p.get("id") == pid});
		    this.fl = new FunctionList(pack.get("functions"));
		    this.flv = new FunctionListView({model:this.fl});
		    this.flv.render();
		},
		render: function (flist) {
		    var ftemps = flist.map(function(f){
			    var temp = $("#packagelist").html();
			    return temp.format(f.get("id"), f.get("name"));
			});
		    this.$el.html(ftemps);
		    this.$el.show();
		},
	    });
	var pl = new PackageList();
	var plv = new PackageListView({model:pl});
	pl.fetch({success:function(data){return plv.render(data)}});
	//	fl.fetch({success:function(data){return flv.render(data)}});
    });
