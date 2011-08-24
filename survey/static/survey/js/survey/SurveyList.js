Ext.ns('Survey.Data', 'Survey.UI', 'Survey.Handler');
//------------------------------------------
// datastore
//------------------------------------------
Survey.Data.SurveyListStore = function(){
    return new Ext.data.GroupingStore({
        reader: new Ext.data.JsonReader({
            idProperty: 'id',
            root: 'data',
            totalProperty: 'results',
            fields: ['id', 'title', 'slug']
        }),
        writer: new Ext.data.JsonWriter({
            encode: true
        }),
        sortInfo: {
            field: 'id',
            direction: 'ASC' // or 'DESC' (case sensitive for local sorting)
        },
        autoLoad: true,
        remoteSort: true,
        restful: true,
        proxy: new Ext.data.HttpProxy({
            url: _baseUrl + 'surveys',
            method: 'GET'
        })
    });
};
//------------------------------------------
// ui
//------------------------------------------


Survey.UI.SurveyListColumnModel = function(){
    return ([{
        header: 'title',
        dataIndex: 'title',
        sortable: true,
        width: 60
    }]);
};

Survey.UI.SurveyList = function(){
    return {
        xtype: 'grid',
        region:'west',
        width:170,
        split: true,
        showBbar: true,
		id:'survey-list',
        tbar: [{
            iconCls: 'silk-arrow-refresh',
            tooltip: 'Rafraichir',
            scope: this,
            handler: function(btn, ev){
                var grid = btn.ownerCt.ownerCt;
                grid.getStore().reload();
            }
        }],
        loadMask: false,
        sm: new Ext.grid.RowSelectionModel({
            singleSelect: true,
            listeners: {
                selectionchange: function(sm){
                	if (sm.hasSelection()) {
                		var record = sm.getSelected();
                        Ext.ux.msgBus.publish('survey.selected', record.data.id);
                	}
                	
                }
            }
        }),
        cm: new Ext.grid.ColumnModel(Survey.UI.SurveyListColumnModel()),
        view: new Ext.grid.GroupingView({
            hideGroupedColumn: false,
            forceFit: true,
            groupTextTpl: '{text} ({[values.rs.length]} {[values.rs.length > 1 ? "éléments" : "élement"]})'
        }),
        listeners: {
            rowdblclick: function(grid, index, e){
                var sm = grid.getSelectionModel();
                if (sm.hasSelection()) {
                    var record = sm.getSelected();
                }
            }
        },
        store: Survey.Data.SurveyListStore()
    };
};

