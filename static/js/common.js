$(document).ready(function(){
    document.addEventListener('play', function(e){
        $('audio').each(function(index, value){
            if(this != e.target)
                this.pause()
        })
    }, true);
    $('[type=search]').keyup(function(e){
        if(e.keyCode == 13){
            if(this.value && this.value.trim().length){
                window.location.href='/tracks?search='+this.value;
            }
        }
    })
})
$.fn.modalRate = function(){
    this.on('click',function(){
        let song = $(this.parentNode.parentNode).find('[name=track]').html()
        $('[name=modal]').find('.modal-content').html(`<div class='modal-header'><h4 class='modal-title font-weight-normal'>Cast your vote for track: ${song}?</h4><button type='button' class='close text-info' data-dismiss='modal'>&times;</button></div><div class='modal-body'><div class='row'><h6 class='col-sm-2 align-auto'>Rate here:</h6><input class='col-sm-6 mt-1 custom-range' type='range' name='rating' min='0' max='10' value='10'><h6 class='col-sm-1 align-auto mr-3' name='points'>10</h6><button class='col-sm-2 btn-info rounded-pill shadow' name='rated'>Submit</button></div></div>`)
        $('[name=rating]').showPoints('points')
        $('[name=rated]').on('click', function(){
            $.ajax({
                 type: 'POST',
                 url: '/ajax/rated',
                 data: { 'song' : song, 'rate' : $(this.parentNode).find('[name=points]').html() },
                 success: function (data) {
                    $('.alert').find('.h5').html(data.response)
                    $('.alert').show()
                    window.scrollTo(0, 0)
                    window.setTimeout(function(){ location.reload() }, 3000)
                 },
                 error: function () {
                    $('.alert').find('.h5').html("Unable to submit your rate! Try again later.")
                    $('.alert').show()
                    window.scrollTo(0, 0)
                 }
            });
            $('[name=modal]').modal('hide')
        })
        $('[name=modal]').modal('show')
    })
}
$.fn.showPoints = function(name){
    this.on('input',function(){
        $(this.parentNode).find(`[name=${name}]`).html(this.value)
    })
}