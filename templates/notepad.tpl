<!DOCTYPE html>
<html>

<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>👁 Märkmik</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/bulma/0.7.2/css/bulma.min.css">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/toastr.js/latest/toastr.min.css" rel="stylesheet"/>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script> 
    <script src="https://cdnjs.cloudflare.com/ajax/libs/toastr.js/latest/toastr.min.js"></script>
    <script defer src="https://use.fontawesome.com/releases/v5.3.1/js/all.js"></script>
</head>

<body>

    <div class="container is-fluid">
        <h1 class="has-text-centered is-size-3">Märkmik</h1>
        <textarea class="textarea is-primary" name="notepadtext" form="markmik">{{tekst}}</textarea>
        <form action="/updatenotepad" id="markmik" method="post" enctype="multipart/form-data">
            <input class="input is-rounded is-hidden" value="{{kasutajanimi}}" type="text" name="kasutajanimi" />
            <input class="input is-rounded is-hidden" value="{{parool}}" type="password" name="parool" />


            <div class="container has-text-centered">
                <input type="submit" class="button is-primary" value="Salvesta" />
            </div>

        </form>

    </div>
    <style>
        .textarea {
            height: 590px;
        }
        @media only screen and (max-width: 600px) {
            .textarea {
                height: 450px;
            }
        }
        .is-hidden {
            display: None;
        }
        .button {
            margin-top: 20px;
        }
    </style>
    <script>

        (() => {if(performance.navigation.type == 2){
            location.reload(true);
        }})() //vajalik selleks, et "tagasi" nuppu vajutades form puhas oleks
        toastr.success('Salvestatud', '', {timeOut: 1500})

    </script>
</body>