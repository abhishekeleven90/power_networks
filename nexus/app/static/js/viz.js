<script src="./plugins/sigma.layouts.forceAtlas2/worker.js"></script>
<script src="./plugins/sigma.layouts.forceAtlas2/supervisor.js"></script>
<script src="./plugins/sigma.layouts.forceLink/supervisor.js"></script>
<script src="./plugins/sigma.layouts.forceLink/worker.js"></script>
<script src="./plugins/sigma.plugins.animate/sigma.plugins.animate.js"></script>
<script src="./plugins/sigma.plugins.filter/sigma.plugins.filter.js"></script>
<script src="./plugins/sigma.plugins.tooltips/sigma.plugins.tooltips.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/mustache.js/0.8.1/mustache.min.js"></script>

<script type="text/javascript">
    //var cyphertext = {{temptext}}
    var initSigma = new sigma ({renderer: {
        container: document.getElementById('graph-container'),
        type: 'canvas'
    },
    settings: {
        labelThreshold: 20,
        defaultLabelSize: 13,
        labelSize: 'fixed',  
        drawEdgeLabels: true,
        minNodeSize: 1.0,
        maxNodeSize: 25.0,
        maxEdgeSize: 2.1,   
        labelAlignment: 'center',
        dragNodeStickiness: 0.01,
        minArrowSize: 15,
        drawEdges: true,
        enableHovering: true,
        sideMargin: 2,
        scalingMode: 'outside',
        animationsTime: 1000,
        enableHovering: true, 
        defaultEdgeLabelSize: 12,
        edgeLabelSize: 'fixed',
        edgeLabelThreshold: 2.0,
    }});


    function customiseGraph(s) {            
        s.graph.nodes().forEach(function(n) {       
            if (n.neo4j_labels[0] == 'Politician'){
            n.color = '#4acfc8'; 
            }
            if (n.neo4j_labels[0] == 'Party'){
            n.color = '#FF6C7C';
            }
            //add more colors according to various labels
            if (n.neo4j_labels[0] == 'Politician')
                n.label = n.neo4j_data.Candidate;
            else n.label = n.neo4j_data.Party;

            n.keys = [];
            n.vals = [];
            var ptable = [];
            for(var k in n.neo4j_data){
                //n.keys.push(k);
                //n.vals.push(n.neo4j_data[k]);
                ptable.push({key: k, val: n.neo4j_data[k]});

            }
            //console.log("Table length="+ptable.length);
            n.data = {props:ptable};
            n.data.getkey = function(){
                return this.key;
            }
            n.data.getval = function(){
                return this.val;
            }
            console.log(n.data);

            n.type = n.neo4j_labels[0];
            n.size = 16.0;
            n.fixed = false;         
    });

    s.graph.edges().forEach(function(n) {
        n.color = '#989898';        
        n.size = 2.1;
    });

    var config = {
      node: {
        show: 'hovers',
        hide: 'hovers',
        cssClass: 'sigma-tooltip',
        position: 'top',
        template:
        '<div class="arrow"></div>' +
        ' <div class="sigma-tooltip-header">{{type}}</div>' +
        '  <div class="sigma-tooltip-body">' +
        '    <table>' +
        '      {{#data.props}}<tr><th>{{data.getkey}}</th> <td>{{data.getval}}</td></tr> {{/data.props}}' +
        '    </table>' +
        '  </div>' +
        '  <div class="sigma-tooltip-footer">Connections: {{degree}}</div>',
        renderer: function(node, template) {
          node.degree = this.degree(node.id);
          return Mustache.render(template, node);
        }
      }
    };

    var tooltips = sigma.plugins.tooltips(initSigma, initSigma.renderers[0], config);
        var fa = sigma.layouts.configForceLink(initSigma, {
         linLogMode: false, 
         adjustSizes: true,
         worker: true,
         autoStop: true,
         background: true,
         scaleRatio: 3,
         gravity: 2,
         easing: 'cubicInOut',
         nodeSiblingsScale: 5,
         barnesHutOptimize: true,
        });

    sigma.layouts.startForceLink();
    var cam = initSigma.camera;
    sigma.misc.animation.camera(cam, { 
        ratio: 1.9
        });
    initSigma.refresh();
    }  
    
    sigma.neo4j.cypher(
            { url: 'http://localhost:7474', user: 'neo4j', password: 'admin' },
              cyphertext,
              initSigma,
              customiseGraph,
              function(s) {
                console.log('Number of nodes :'+ initSigma.graph.nodes().length);
                console.log('Number of edges :'+ initSigma.graph.edges().length);
            }
    );

    var activeState = sigma.plugins.activeState(initSigma);
    var dragListener = sigma.plugins.dragNodes(initSigma, initSigma.renderers[0], activeState);
    var select = sigma.plugins.select(initSigma, activeState);
    var keyboard = sigma.plugins.keyboard(initSigma, initSigma.renderers[0]);
    select.bindKeyboard(keyboard);
</script>

