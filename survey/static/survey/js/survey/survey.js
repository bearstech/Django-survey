Ext.ns('Survey.Data', 'Survey.UI', 'Survey.Handler');

Ext.onReady(function() {
	Ext.QuickTips.init();
	Ext.ux.msgBus = new Ext.ux.MessageBus();

	var viewport = new Ext.Viewport({
		layout : 'fit',
		items : [ {
			layout : 'border',
			border : false,
			items : [ Survey.UI.SurveyList(), Survey.UI.QuestionList(), {
				layout : 'border',
				region:'east',
				width:700,
				split: true,
				items : [ Survey.UI.QuestionDetails(), Survey.UI.ChoiceList() ]
			}]
		} ]
	});
});