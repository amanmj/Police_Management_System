  function deleteTemplate(caller,item_slug){
    var csrftoken = getCookie('csrftoken');
    $.ajax({
      url:'/deleteTemplate/'+item_slug+'/',
      type:"POST",
      data:{'slug':item_slug,'csrfmiddlewaretoken':csrftoken},
      success:function(res){
        // console.log('Successfully deleted!');
        $.amaran({'message':'Successfully deleted the template.'});
        console.log($(caller).parent('.card'));
        $(caller).parents('.card').remove();
      }
    });
  }

  $(document).ready(function(){

    $('.ui.form')
      .form({
        fields: {
          name: {
            identifier : 'name',
            rules: [
              {
                type   : 'empty',
                prompt : 'Please enter a password'
              }
            ]
          },
          slug: {
            identifier : 'slug',
            rules: [
              {
                type   : 'regExp[/^[a-z0-9-]+$/]',
                prompt : 'Enter a valid Slug'
              }
            ]
          }
        },
        onSuccess:function(event,fields){
          event.preventDefault();
          console.log('hey');
          $('#createTemplate').addClass('loading');
          $('#createTemplate').attr('disabled',true);
          fields.type='mockup';
          // console.log(fields);
          $.post('/choose', fields,function(){
              console.log('yo');
            },'json')
          .done(function(data){
            $('#createTemplate').removeClass('loading');
            $('#createTemplate').attr('disabled',false);
            console.log(data);
            if(data.success===true){
              $('#mockupForm')[0].reset();
              $('.ui.modal').modal('hide');

              //Append created template to DOM
              var x=$('#templateToInsert').html();
              var template=$(x);
              template.find('.createdName').html(data.template.name);
              template.find('.createdName').attr('href',"/showcase/"+data.template.user+"/"+data.template.name);
              template.find('.createdSlug').append(data.template.slug);
              template.find('.createdDescription').html(data.template.description);
              template.find('.createdLink').attr('href','/editor/'+data.template.slug);
              template.appendTo('#templatesContainer');
            }
            $.amaran({'message':data.message});
          });
          
            // console.log(data.errors);
             // $('.message').html(data.message);
             // of course you can do something more fancy with your respone
          return false;
        }
      });
      
    
    $('.special.cards .image').dimmer({
      on: 'hover'
    });

    $('.chooseMockup').on('click',function(e){
      $('#mockupId').val($(e.target).data('mockupid'));
      // console.log($(e.target).data('mockupid'));
      $('.ui.modal.chooseMockupModal').modal('show');
    });

    $('.closeModal').on('click',function(){
      $('.ui.modal.chooseMockupModal').modal('hide');
    });


    // $.get('/templates')
    // .done(function(data){
    //   console.log(data);
    // });







  });