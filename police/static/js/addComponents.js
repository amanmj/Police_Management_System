var componentMode,tableColumnCount=1;
function insertTemplate(templateId){
	templateId="'#"+templateId+"'";
	$(target).html($(templateId).html);
}

function readURL(input) {
   if (input.files && input.files[0]) {
       var reader = new FileReader();

       reader.onload = function (e) {
           $('#blah')
               .attr('src', e.target.result)
               .width(150);
       };
       reader.readAsDataURL(input.files[0]);
   }
}

var angreejiCounting=['zero','one','two','three','four','five','six','seven','eight','nine','ten','eleven','twelve','thirteen','fourteen','fifteen','sixteen'];

function resizer(e){
	e.resizable({handles:'e'}).bind({
		resizestart:function(event,ui){
			$(event.target).attr('class','column');
		},
		resizestop:function(event,ui){
			var widthOfOneDiv=$('.columnSetup>.column').outerWidth();
			var widthOfResizable=$(event.target).width();
			var x=Math.round(widthOfResizable/widthOfOneDiv);
			$(event.target).addClass(angreejiCounting[x]+' wide column').css('width','');
		}
	});
}



function getDivSizes(){
	var divSizes=[];
	$('.sizeSelector>.column').each(function(){
		divSizes.push($(this).attr('class').replace('ui-resizable',''));
	});
	console.log(divSizes);
	return divSizes;
}

function inserter(x){
	switch(componentMode){
		case 'after':
			$(x).insertAfter($('.selected-area'));
			break;
		case 'before':
			$(x).insertBefore($('.selected-area'));
			break;
		case 'into':
			$(x).appendTo($('.selected-area'));
			break;
		default:
			console.log('WTF! Chu hai kya be :|');
	}
}

function insertGrid(divSizes){
	var x=	$('<div class="ui container ab grid edit-area edit-area--div paint-area grid" style="margin:0"></div>');
	divSizes.forEach(function(yo){
		yo+=' edit-area paint-area';
		$('<div></div>').addClass(yo).append('<div class="paint-area paint-area--text edit-area edit-area--text" style=" ">hello-again-bc</div>').appendTo(x);
	});

	inserter(x);
}
function insertDiv(){
	var divSize=$('.divSizeSelector>.column').attr('class').replace('ui-resizable','');
	var x=$('<div></div>').addClass(divSize+' edit-area paint-area').append('<div class="paint-area paint-area--text edit-area edit-area--text" style=" ">hello-again-bc</div>');
	inserter(x);
}
function insertImage(url){
	var x=$('<div class="edit-area image-resizable image-div" style="overflow:hidden;width:200px;height:200px;">\
		<img class="ui fluid image">\
		</div>');
	x.children('img').attr('src',url);
	inserter(x);
	x.resizable({handles:'e, s'}).bind({
		resizestart:function(event,ui){
			// $(event.target).attr('class','column');
			console.log('yo');	
		},
		resizestop:function(event,ui){
			// var widthOfOneDiv=$('.columnSetup>.column').outerWidth();
			// var widthOfResizable=$(event.target).width();
			// var x=Math.round(widthOfResizable/widthOfOneDiv);
			// $(event.target).addClass(angreejiCounting[x]+' wide column').css('width','');
		}
	});
}

function insertTable(){
	var x=$('<table class="ui compact celled single line table edit-area edit-area--table"></table>');
	var tableHead=$('<thead><tr></tr></thead>');
	var tableBody=$('<tbody><tr></tr></tbody>');
	// var tableRow=$('<thead><tr></tr><thead>');
	for(i=1;i<=tableColumnCount;i++)
	{
		$('<th></th>').html('header'+i).appendTo(tableHead.children('tr'));
		$('<td></td>').html('content'+i).appendTo(tableBody.children('tr'));
	}
	tableHead.appendTo(x);
	tableBody.appendTo(x);
	// console.log(x.html());

	inserter(x);
	// y.appendTo(x);
	// console.log(x.html());
}
function insertRow(){
	var tableRow=$('<tr></tr>');
	var tableColumns=$('.selected-area>thead th').length;
	console.log(tableColumns);
	for(i=1;i<=tableColumns;i++)
	{
		$('<td></td>').html('content'+i).appendTo(tableRow);
	}
	tableRow.appendTo($('.selected-area').children('tbody'));
}
$(document).ready(function(){


	function init(){
		//SET INSERT MODE
		componentMode=$('.insertModeButton.active').data('mode');
		$('.insertModeButton').click(function(){
			$(this).addClass('active').siblings('.button').removeClass('active');
			componentMode=$(this).attr('data-mode');
		});

		//SET DIVS IN GRID
		$('#divsCount').change(function(){
			var count=$(this).val();
			var temp=count,x=0,opacity=0.2;
			$('.sizeSelector').html('');
			while(temp--)
			{
				x=16/count;
				x=Math.floor(x);
				var e=$('<div class="'+ angreejiCounting[x]+ ' wide column" style="opacity:'+opacity+'"></div>');
				resizer(e);
				$('.sizeSelector').append(e);
				opacity+=0.15;
			}
		});

		//INTIALIZE DIV RESIZE - GRID
		resizer($('.sizeSelector>.column'));


		//INSERT GRID BUTTON
		$('.insert-grid').click(function(){
			var divSizes=getDivSizes();
			insertGrid(divSizes);
		});


		//DIV INSERT INIT
		$('.divSizeSelector>.column').resizable({handles:'e'}).bind({
			resizestart:function(event,ui){
				$(event.target).attr('class','column');
			},
			resizestop:function(event,ui){
				var widthOfOneDiv=$('.divColumnSetup>.column').outerWidth();
				var widthOfResizable=$(event.target).width();
				var x=Math.round(widthOfResizable/widthOfOneDiv);
				$(event.target).addClass(angreejiCounting[x]+' wide column').css('width','');
			}
		});

		//INSERT DIV BUTTON
		$('.insert-div').click(function(){
			insertDiv();
		});

		//INIT IMAGE RESIZE

		// console.log($('div.image-resizable'));
		// $('div.image-resizable').resizable({handles:'e, s'}).bind({
		// 	resizestart:function(event,ui){
		// 		// $(event.target).attr('class','column');
		// 		console.log('yo');	
		// 	},
		// 	resizestop:function(event,ui){
		// 	}
		// });

		//INSERT IMAGE
		$('#imageForm').submit(function(e){
			console.log('Image form is submitted! Moving one step forward :)');
		    e.preventDefault();
		    var data = new FormData(this);
		    $.ajax({
		    	url:'/insertImage',
		    	data:data,
		    	cache:false,
		    	processData:false,
		    	contentType:false,
		    	// contentType:'multipart/form-data',
		    	type: 'POST',
		    	dataType:'json',
		    	success:function(data){
		    		console.log(typeof(data));
		    		insertImage(data.url);
		    	}
		    });
		});

		//TABLE-COLUMNS COUNT
		$('#tableColumnsCount').on('change',function(){
			tableColumnCount=$(this).val();
			if(tableColumnCount>6) 
				tableColumnCount=6;
			// console.log(tableColumnCount);
		});
		//INSERT TABLE
		$('.insert-table').click(function(){
			insertTable();
		});
		//TABLE EDIT
		$('body').on('dblclick','.edit-area--table td,.edit-area--table th',function(e){
			console.log('working! Ab kal karenge...');
			var Text=$(this).html().trim().replace(/(<br>)|(<br \/>)|(<p>)|(<\/p>)/g, "\n");
			var editableText=$('<input class=""></input>');
			editableText.val(Text);
			$(this).html(editableText);
			editableText.focus();
			editableText.blur(function(){
				var inputVal=$(this).val();
				console.log(inputVal);
				$(this).parent().html(inputVal);
			});
		});

		//TABLE-MENU
		$("#tableMenu li").click(function(){
		    
		    // This is the triggered action name
		    switch($(this).attr("data-action")) {
		        case "delete": $('.selected-area').remove(); break;
		        case "insertRow": insertRow(); break;
		        case "deleteRow": console.log('deleting');$('.selected-area .currentRow').remove();break;
		    }
		  	
		    // Hide it AFTER the action was triggered
		    $(".custom-menu").hide(100);
		  });
		//TABLE-DELETE-ROW-INIT
		$('body').on('click','.edit-area--table tr',function(){
			$(this).parents('table').find('tr').removeClass('styleTr currentRow');
			$(this).addClass('styleTr currentRow');
		});
		
	}
	init();
	$('.ui.accordion').accordion();
});