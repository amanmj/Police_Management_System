function extractCss(){
	var elem=$('.selected-area');
	var x={};
	x.border={};
	x.padding={};
	x.margin={};
	x.fontSize=elem.css('font-size');
	x.border.width=elem.css('border-width');
	x.border.style=elem.css('border-style');
	x.border.color=elem.css('border-color');
	x.textAlign=elem.css('text-align');
	x.background=elem.css('background');
	//PADDING
	x.padding.top=elem.css('padding-top');
	x.padding.left=elem.css('padding-left');
	x.padding.bottom=elem.css('padding-bottom');
	x.padding.right=elem.css('padding-right');
	//MARGIN
	x.margin.top=elem.css('margin-top');
	x.margin.left=elem.css('margin-left');
	x.margin.bottom=elem.css('margin-bottom');
	x.margin.right=elem.css('margin-right');
	console.log(x.margin);
	return x;
}

function normalizeVal(a)
{
	return a.replace(/[^-\d\.]/g, '');
}
var selectedAreaCss={};


String.prototype.nl2br = function()
{
    return this.replace(/\n/g, "<br>");
};

$(document).ready(function(){

	$('.ui.dropdown').dropdown();
	//Sidebar Buttons-Settings and components
	var dataVal=$('.editorButtons>div.ui.button.activeButton').data('value');
	$('.editorButtons>div.ui.button.activeButton').removeClass('inverted basic').siblings('.ui.button').removeClass('activeButton').addClass('inverted basic');
	$(".sidebarMainDiv[data-value='"+dataVal+"']").removeClass('hideIt').addClass('showIt').siblings('.sidebarMainDiv').removeClass('showIt').addClass('hideIt');

	function editSelectedTextArea(){
		var divText=$('.edit-area--text.selected-area').html().trim().replace(/(<br>)|(<br \/>)|(<p>)|(<\/p>)/g, "\n");
		var editableText=$('<textarea class="edit--text---textbox"></textarea>');
		editableText.val(divText);
		$('.selected-area.edit-area--text').html(editableText);
		editableText.focus();	
		$('.edit-text-button').off();
		editableText.blur(editableTextBlurred);
	}
	function editableTextBlurred(){
		var divVal=$(this).val().nl2br();
		if(divVal===""||divVal===null)
			$('.selected-area.edit-area--text').remove();
		else
			$('.selected-area.edit-area--text').html(divVal);
	}
	function fontSizeChange(target){
		var elem=$('.selected-area');
		var incordec=$(target).data('fontsize');
		if(incordec==="increase"){
			elem.animate({'font-size':'+=1'},100);
			elem.animate({'line-height':'+=1'},100);
		}
		else{
			elem.animate({'font-size':'-=1'},100);
			elem.animate({'line-height':'-=1'},100);
		}
	}
	function setBorderSettings(){
		$('.borderWidthSetting').val(normalizeVal(selectedAreaCss.border.width));
		
		$('.borderStyleDropdown').dropdown('set selected',selectedAreaCss.border.style);
		$('.borderStyleDropdown').dropdown({onChange:function(value,text){
			$('.selected-area').css('border-style',value);
		}});
		// $('.borderStyleDropdown').change(function(e){
		// 	var selectedStyle=$('.borderStyleDropdown').dropdown('get value');
		// 	$('.selected-area').css('border-style',selectedStyle);
		// });
		$('.borderWidthSetting').change(function(e){ 
			$('.selected-area').css('border-width',this.value+'px');
			// console.log($('.selected-area').css('border-width'));
		});
	}
	function setPadding(){
		$('.setPadding[data-position="top"]').val(normalizeVal(selectedAreaCss.padding.top));
		$('.setPadding[data-position="left"]').val(normalizeVal(selectedAreaCss.padding.left));
		$('.setPadding[data-position="bottom"]').val(normalizeVal(selectedAreaCss.padding.bottom));
		$('.setPadding[data-position="right"]').val(normalizeVal(selectedAreaCss.padding.right));
		$('.setPadding').change(function(e){
			var $this=$(this);
			var position='padding-'+$this.data('position');
			$('.selected-area').css(position,$this.val()+'px');
		});	
	}
	function setMargin(){
		$('.setMargin[data-position="top"]').val(normalizeVal(selectedAreaCss.margin.top));
		$('.setMargin[data-position="left"]').val(normalizeVal(selectedAreaCss.margin.left));
		$('.setMargin[data-position="bottom"]').val(normalizeVal(selectedAreaCss.margin.bottom));
		$('.setMargin[data-position="right"]').val(normalizeVal(selectedAreaCss.margin.right));
		if($('.selected-area').hasClass('container')){
			$('.setMargin[data-position="left"]').prop('disabled',true);
			$('.setMargin[data-position="right"]').prop('disabled',true);
		}
		else{
			$('.setMargin[data-position="left"]').prop('disabled',false);
			$('.setMargin[data-position="right"]').prop('disabled',false);
		}
		$('.setMargin').change(function(e){
			var $this=$(this);
			var position='margin-'+$this.data('position');
			$('.selected-area').css(position,$this.val()+'px');
		});	
	}
	function customMenu(){

		//Right click action on selected-area
		$(document).on("contextmenu",'.selected-area', function (event) {
		    // Avoid the real one
		    event.preventDefault();		    
		    // Show contextmenu
		    if($(this).hasClass('edit-area--table')){
		    	console.log($(this));
		    	$('#tableMenu').finish().toggle(100).css({
		        	top: event.pageY + "px",
		        	left: event.pageX + "px"
		    	});
		    }
		    else{
		    	$("#generalMenu").finish().toggle(100).css({
		        	top: event.pageY + "px",
		        	left: event.pageX + "px"
		    	});
		    }
		    // In the right position (the mouse)

		});


		// If the document is clicked somewhere
		$(document).bind("mousedown", function (e) {
		    // If the clicked element is not the menu
		    if (!($(e.target).parents(".custom-menu").length > 0)) {
		        // Hide it
		        $(".custom-menu").hide(100);
		    }
		});


		// If the menu element is clicked
		$("#generalMenu li").click(function(){
		    
		    // This is the triggered action name
		    switch($(this).attr("data-action")) {
		        
		        // A case for each action. Your actions here
		        case "delete": $('.selected-area').remove(); break;
		        // case "insertInto":$('.selected-area'
		    }
		  
		    // Hide it AFTER the action was triggered
		    $(".custom-menu").hide(100);
		  });
		
		//Display inner menu on hover
		$('.custom-menu li[data-innerMenu]')
		.mouseenter(function(){
			var innerMenuName=$(this).attr('data-innerMenu');
			$('.custom-menu-inner[data-innerMenu="'+innerMenuName+'"]').show(300);
		})
		.mouseleave(function(){
			var innerMenuName=$(this).attr('data-innerMenu');
			$('.custom-menu-inner[data-innerMenu="'+innerMenuName+'"]').hide(200);
		});

	}

	function init_settings(){
		customMenu();

		$(document).on('click','.edit-area',function(e){
			//console.log(this);
			$('.edit-area').removeClass('selected-area');
			$(this).addClass('selected-area');
			selectedAreaCss=extractCss();
			// console.log(selectedAreaCss);
			
			setBorderSettings();
			setPadding();
			setMargin();

			$('.onlyVisibleOnSelectedDiv').css('display','block');
			e.stopPropagation();
			if($(this).hasClass('edit-area--text')){
				$('.edit-text-button').remove();
				$('.onlyVisibleOnSelectedDiv').append('<button class="ab edit-text-button ui button inverted" style="margin-left:10px;">EDIT</button>');
			}
			else{
				$('.edit-text-button').remove();

			}
			if($(this).hasClass('wide column')){
				// console.log('show karo');
				$('.divSelectorContainer').removeClass('transparentIt');
			}
			else{
				// console.log('hide karo');
				$('.divSelectorContainer').addClass('transparentIt');
			}
		});

		//ALIGNMENT
		var abAlignClasses = new RegExp('\\b' + 'ab-align-' + '.+?\\b', 'g');
		$('.alignmentButton').click(function(){
			$('.selected-area')[0].className=$('.selected-area')[0].className.replace(abAlignClasses,'');
			// classie.add('.selected-area','ab-align-'+$(this).data('align'));
			$('.selected-area').addClass('ab-align-'+$(this).data('align'));	
		});

		//FONT-SIZE
		$('.fontSizeChange').click(function(e){
			fontSizeChange(e.target);
		});

		//FONT-STYLE
		var abStyleClasses = new RegExp('\\b' + 'ab-style-' + '.+?\\b', 'g');
		$('.styleButton').click(function(){
			// $('.selected-area')[0].className=$('.selected-area')[0].className.replace(abStyleClasses,'');
			$('.selected-area').toggleClass('ab-style-'+$(this).data('style'));	
		});

		//BORDER
		
		//PADDING
		
		//MARGIN

		//EDIT-TEXT
		$('.onlyVisibleOnSelectedDiv').on("click",".edit-text-button",function(){
			editSelectedTextArea();
		});


	}

	// init();

	$('.colorSelectButton').click(function(){
		if($('#colorBox').hasClass('hideIt')){
			$('#colorBox').addClass('showIt').removeClass('hideIt');
		}
		else
			$('#colorBox').removeClass('showIt').addClass('hideIt');
	});	
	
 	$('#colorpicker').farbtastic(function(){
		$('.color-x').css('background',$.farbtastic('#colorpicker').color);
		$('#colorPickerDragElement').attr('data-color',$.farbtastic('#colorpicker').color);
	});
	$('.editorButtons>div.ui.button').click(function(){
		var dataValue=$(this).data('value');
		$(this).removeClass('inverted basic').addClass('activeButton').siblings('.ui.button').removeClass('activeButton').addClass('inverted basic');
		$(".sidebarMainDiv[data-value='"+dataValue+"']").removeClass('hideIt').addClass('showIt').siblings('.sidebarMainDiv').removeClass('showIt').addClass('hideIt');
	});
	$('.closeTool').click(function(){
		//	console.log($(this).parents('.settingBox'));
		$(this).parents('.settingBox').addClass('hideIt');
	});

	//SETTINGS INITIALIZE
	init_settings();
});