/**
 * Copyright 2018, Google LLC
 * Licensed under the Apache License, Version 2.0 (the `License`);
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *    http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an `AS IS` BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
 
// [START gae_python38_log]
// [START gae_python3_log]
'use strict';

window.addEventListener('load', function () {

  console.log("Hello World!");

});
function submitQueryForm() {
  var title = document.getElementById("title").value;
  console.log(title)
  // document.getElementById("hidden_title").value = title;

  var year = $.trim($("year1").val())
}
function subcribe(){
  $.ajax({
    url:"{{ url_for('subscribe') }}",
    type:"POST",
    // data:{
    //   'row':row
    // }

  })
}
// [END gae_python3_log]
// [END gae_python38_log]
