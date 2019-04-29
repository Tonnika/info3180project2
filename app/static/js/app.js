Vue.component('app-header', {
    template: `
    <nav class="navbar narvbar-expand-lg navbar-dark bg-primary fixed-top">
        <img src='static/img/applogo.jpg' class="small-logo"/>
        <a class="navbar-brand" href="#">Photogram</a>
        <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
        </button>
        
        <div class="collapse navbar-collapse" id="navbarSupportedContent">
            <ul class="navbar-nav mr-auto">
            </ul>
        </div>
        
            <ul class="navbar-nav">
                <li class="nav-item active">
                    <router-link class="nav-link" to="/">Home <span class="sr-only">(current)</span></router-link>
                </li>
                <li class="nav-item active">
                    <router-link class="nav-link" to="/explore">Explore</router-link>
                </li>
                <li class="nav-item active">
                    <router-link class="nav-link" :to="{name: 'users', params: {user_id: activeuser}}">My Profile</router-link>
                </li>
                <li v-if="auth" class="nav-item">
                    <router-link class="nav-link active" to="/logout">Logout</router-link>
                </li>
                <li v-else class="nav-item">
                    <router-link class="nav-link active" to="/login">Login</router-link>
                </li>
            </ul>
    </nav>
    `,
    data: function(){
    return {
        auth: localStorage.hasOwnProperty("current_user"),
        activeuser: localStorage.hasOwnProperty("current_user") ? JSON.parse(localStorage.current_user).id : null
    }
    }
});

Vue.component('app-footer', {
    template: `
    <footer>
        <div class="container">
        
        </div>
    </footer>
    `
});

const Home = Vue.component('home', {
    template: `
    <div class= "row landing-container">
        div class="col-md-4 landing-container-child" style="margin-left: 11%;">
            <img src="/static/images/home.jpg" id="home-img"/>
    </div>
    <div class="col-md-4 landing-container-child float-clear">
        <div class="card" style="width:28rem; height: 23rem; box-shadow: 2px 2px 10px grey;">
            img class="card-img-top" src="static/img/applogo.jpg" alt="Card image cap" style="width:60%; margin: 0 auto; padding-top:20px;">
            <div class="card-body" style="padding-top: 0px;">
                <hr>
                <p class="card-text">Share memories with your friends</p>
                <div style="margin-top: 20%;">
                    <router-link class="btn btn-success col-md-5" to="/register">Register</router-link>
                    <router-link class="btn btn-primary col-md-5" to="/login">Login</router-link>
                </div>
            </div>
        </div>
    </div>
</div>

    `,
    data:function() {
        return {}
    }
});

const Login = Vue.component('login', {
    template: `
    <div>
        <form id="login-html" @submit.prevent="login">
            <div class="card-header center">
              <strong>Login</strong>
            </div>
            <div class="card center">
              <div class="card-body login">
                <div style="margin-top:5%;">
                  <label for='username'><strong>Username</strong></label><br>
                  <input type='text' id='username' name='username' style="width: 100%;"/>
                 </div>
                 <div style="magin-top:5%;">
                   <label for ='password'><strong>Password</strong></label><br>
                   <input type='password' id='password' name='password' style="width: 100%;"/>
                  </div>
                  <div v-if="messageFlag' style="margin-top:5%;">
                    <div class="alert alert-danger center" style="width: 100%; margin-top:5%;">
                      {{ message }}
                    </div>
                </div>
            </div>
        </div>
    </form>
</div>
    `,
    methods:{
        login: function(){
            const self = this 
            
            let login_data = document.getElementById('login-html');
            let login_html = new FormData(login_data);
            
            fetch("/api/auth/login",{
                method:"POST",
                body: login_html,
                headers: {
                'X-CSRFToken': token
                },
                credentials: 'same-origin'
            }).then(function(jsonResponse){
                return response.json();
            }).then(function(jsonResponse){
                self.messageFlag = true;
                
                if(jsonResponse.hasOwnProperty("token")){
                    activeuser={"token":jsonResponse.token, id: jsonResponse.user_id};
                    localStorage.current_user = JSON.stringify(currentuser);
                    
                    router.go()
                    router.push("/explore")
                }else{
                    self.message = jsonResponse.errors
                }
            }).catch(function(error){
                self.messageFlag = false;
                console.log(error);
            });
        }
    }, 
    data: function(){
        return {
            messageFlag: false, 
            message: ""
        }
    }
});

const Logout = Vue.component("logout", {
    template:`
    <div>
    </div>`,
    created: function(){
        const self = this;
    
    fetch("api/auth/logout", {
        method: "GET"
    }).then(function(response){
        return response.json();
    }).then(function(jsonResponse){
        localStorage.removeItem("current_user");
        router.go();
        router.push("/");
    }).catch(function(error){
        console.log(error);
    });
    }
});

const NewPost = Vue.component('posts', {
    template: `
    <div>
        <form class="center" id="postform" @submit.prevent="submit">
            <div class="card-header center"><strong> New Post</strong></div>
            <div class="card center">
                <div class="card-body">
                        <label><strong>Photo</strong></label><br>
                        input id="user_id" name="user_id" v-bind:value="activeuser" style="display: none;"/>
                    <label class="btn" style="border: 0.5px solid black" for="photo"><strong>Browse</strong></label>
                    <label>{{ filename }}</label>
                    <br>
                    <input type = "file" id="photo" name="photo" style="display: none;" v-on:change="updateFilename"/>
                    <label style="margin-top: 5%"><strong>Caption</strong></label><br>
                    <textarea id="caption" name="caption" style="width:100%" placeholder="Caption.."></textarea>
                    <button id="submit" class = "btn btn-success">Submit</button>
            
            <div v-if='messageFlag' >
              <div v-if="errorFlag">
                <div style="width: 100%; margin-top: 5%;">
                  <ul class="alert alert-danger">
                    <li v-for="error in message">
                        {{ error }}
                    </li>
                  </ul>
                </div>
              </div>
              <div v-else class="alert alert-success" style="width: 100%; margin-top: 5%;">
                {{ message }}
              </div>
            </div>
        </div>    
      </div>
    </form>
  </div>
  `,
  methods: {
    updateFilename :function(){
        const self = this
        let filenameArr = $("#photo")[0].value.split("\\");
        self.filename = filenameArr[filenameArr.length-1]
    },
    submit: function(){
      self = this;
      self.messageFlag = true;
      self.message = "Sending Post......";
      
      fetch(`/api/users/${JSON.parse(localStorage.current_user).id}/posts`,{
        method: "POST",
        headers: {
          "Authorization": `Bearer ${JSON.parse(localStorage.current_user).token}`,
          'X-CSRFToken': token
        },
        body: new FormData(document.getElementById("postform")),
        credentials: 'same-origin'
        
      }).then(function(response){
        return response.json();
      }).then(function(jsonResponse){
        
        
        if(jsonResponse.hasOwnProperty("status")){
         if(jsonResponse.status == 201){
            self.errorFlag = false;
            self.message = jsonResponse.message
          }else{
            self.errorFlag = true;
            self.message= jsonResponse.errors;
          } 
        }
      }).catch(function(error){
        self.message = "Error encountered"
        console.log(error);
      });
    }
  },
  data: function(){
    return {
      filename: 'No files',
      messageFlag: false,
      errorFlag: false,
      message: "",
      activeuser: JSON.parse(localStorage.current_user).id
    }
  }
  
});

const Register=Vue.component("register",{
  template:`
        <div>
          
          <h3 class="card-header center text-muted">Register</h3>
          <div class="card center">
           
            <form id="register" @submit.prevent="Register" enctype="multipart/form-data">
            <div>
                <label>Firstname:</label><br/>
                
               <input type='text' id='firstname' name='firstname' style="width: 100%;"/>
            </div>
            <div>
                <label>Lastname:</label><br/>
               <input type='text' id='lastname' name='lastname' style="width: 100%;"/>
            </div>
            <div>
                <label>Username:</label><br/>
               <input type='text' id='username' name='username' style="width: 100%;"/>
               
            </div>
            <div>
                <label>Password:</label><br/>
               <input type='password' id='password' name='password' style="width: 100%;"/>
            </div>
            <div>
                <label>Email:</label><br/>
               <input type='text' id='email' name='email' placeholder="love@example.com" style="width: 100%;"/>
            </div>
            <div>
                <label>Location:</label><br/>
               <input type='text' id='location' name='location' style="width: 100%;"/>
            </div>
            <div>
                <label>Biography:</label><br/>
               <textarea name="biography" rows="3" style="width:100%"> </textarea><br/>
            </div>
            <div>
                <label for='photo' class='btn btn-primary'>Browse....</label> <span>{{ filename }}</span>
                
                <input id="photo" type="file" name='photo' style="display: none" v-on:change = "pushfile" /><br/>
                
            </div>
                
                 <div>
                      <input type="submit" id="submit" class="btn btn-success" value="Sign Up" /> 
                    </div>
                
            </form>
            <div v-if='messageFlag' style="margin-top: 5%;">
            
                <div v-if="!errorFlag ">
                    <div class="alert alert-success" >
                        {{ message }}
                    </div>
                </div>
                <div v-else >
                    <ul class="alert alert-danger">
                        <li v-for="error in message">
                            {{ error }}
                        </li>
                    </ul>
                </div>
                
            </div>
        </div>
    </div>
  `,
   methods: {
      Register : function(){
          let self = this;
          let register = document.getElementById('register');
          let form_data = new FormData(register);
          
          fetch("/api/users/register", {
              method: "POST",
              body: form_data,
              headers: {
              'X-CSRFToken': token
              },
              credentials: 'same-origin'
          }).then(function(response){
              return response.json();
          }).then(function (jsonResponse) {
              // display a success message
              self.messageFlag = true
              
              if (jsonResponse.hasOwnProperty("errors")){
                  self.errorFlag=true;
                  self.message = jsonResponse.errors;
              }else if(jsonResponse.hasOwnProperty("message")){
                  router.push("/login");
              }
        });
      },
      pushfile: function(){
        let self = this
        let filenameArr = $("#photo")[0].value.split("\\");
        self.filename = filenameArr[filenameArr.length-1]
      }
   },
   data: function(){
     return {
        errorFlag: false,
        messageFlag: false,
        message: [],
        filename: "No files"
    }
   }
});

const Explore = Vue.component("explore", {
  template:`
    <div class="row">
      
      <div v-if="postFlag" class="col-md-7" style="margin: 0 auto;">
        <div class="card" style=" width:100%; padding: 0; margin-bottom: 5%" v-for="(post, index) in posts">
          <ul class="list-group list-group-flush">
            <li class="list-group-item">
              <img id="pro-photo" v-bind:src=post.profile_photo style="width:40px"/>
              <router-link class="username" :to="{name: 'users', params: {user_id: post.user_id}}">{{ post.username }}</router-link>
            </li>
            <li class="list-group-item" style="padding: 0;">
              <img id="post-img" v-bind:src=post.photo style="width:100%" />
            </li>
            <li class="list-group-item text-muted">
              {{ post.caption }}
              <div class="row" style="margin-top: 10%">
                <div id="likes" class="col-md-6" style="text-align: left;">
                  <img class="like-ico liked" src="static/icons/liked.png"  v-on:click="Like" style="width:20px; display: none;"/>
                  <img class="like-ico like" src="static/icons/like.png"  v-on:click="Like" style="width:20px;"/> {{post.likes}} Likes
                  
                  <input type="hidden" id="post-id"  v-bind:value="post.id" />
                  <input type="hidden" id="post-index" v-bind:value="index" />
                </div>
                <div id="post-date" class="col-md-6" style="text-align: right">
                  {{post.created_on}}
                </div>
              </div>
            </li>
          </ul>
        </div>
      </div>
      <div v-else>
        <div class="alert alert-primary" >
          No posts yet.
        </div>
      </div>
        
      <div class="col-md-3">
        	<router-link class="btn btn-primary" to="/posts/new" style="width:100%;">New Post</router-link>
      </div>
    </div>
  `,
  created: function(){
    self = this;
    
    fetch("/api/posts", {
      method: "GET",
      headers:{
        "Authorization": `Bearer ${JSON.parse(localStorage.current_user).token}`,
        'X-CSRFToken': token
      },
      credentials: 'same-origin'
    }).then(function(response){
      return response.json();
    }).then(function(jsonResponse){
      if(jsonResponse.hasOwnProperty("posts")){
        if(jsonResponse.posts.length !=0){
          self.posts = jsonResponse.posts.reverse();
          self.postFlag = true;
        }
      }
    }).catch(function(error){
      console.log(error);
    });
  },
  methods: {
    Like: function(event){
      self = this;
      let node_list = event.target.parentElement.children;
      let post_id = node_list[node_list.length-2].value;
      let post_index = node_list[node_list.length-1].value;
      
      fetch(`/api/posts/${post_id}/like`, {
        method: "POST",
        headers: {
          "Authorization": `Bearer ${JSON.parse(localStorage.current_user).token}`,
          'X-CSRFToken': token,
          'Content-Type': 'application/json'
        },
        credentials: "same-origin",
        body: JSON.stringify({"user_id": JSON.parse(localStorage.current_user).id, "post_id": post_id})
      }).then(function(response){
        return response.json();
      }).then(function(jsonResponse){
        
        if(jsonResponse.hasOwnProperty("status")){
          if(jsonResponse.status == 201){
            event.target.style.display="none"
            event.target.previousElementSibling.style.display="";
            self.posts[post_index].likes = jsonResponse.likes;
          }
        }
      }).catch(function(error){
        console.log(error);
      });
    }
  },
  data: function(){
    return {
      posts: [],
      postFlag: false
    }
  }
});

const Profile = Vue.component("profile",{
  template: `
  <div>
    <div class="card row" style="width:100%">
        <div class="card-body row profile-header" style="padding: 0;" >
          <img id="profile_image" class="col-md-2" v-bind:src=user.profile_image style="width: 100%; height: 15%" />
          <div id="profile_info" class="col-md-7" style="margin-top: 0px;padding-right: 0;">
            <strong><label>{{ user.first_name }}</label>
            <label>{{ user.last_name }}</label></strong>
            <div id="local" style="color: gray;">
              <label>{{ user.location }}</label><br>
              <label>{{ user.joined_on }}</label>
            </div>
            <p id="bio" style="color: gray;">
              {{ user.biography }}
            </p>
          </div>
          <div id="follows" class="col-sm-3" style="padding-left:  0; padding-right:  0;">
            <strong><label id="posts" class="col-md-5">{{ user.postCount }}</label>
            <label id="followers" class="col-md-5">{{ user.followers }}</label></strong> <br>
            <label class="col-md-5" style="color: gray; font-weight: 600; font-size: larger;">Posts</label>
            <label class="col-md-6" style="color: gray; font-weight: 600; font-size: larger;">Followers</label>
            <label id="followclick" class="btn btn-primary" v-on:click="follow" style="width:100%; margin-top: 17%;">Follow</label>
          </div>
        </div>
    </div>
    
    <div id="post-area" class="row" style="width:100%;">
      <div class="profile-post col-md-4" style="margin-top:3%;" v-for="post in user.posts">
          <img v-bind:src=post.photo style="width: 100%;" />
      </div>
    </div>
  </div>
  `,
  methods: {
    follow: function(){
      self = this;
      
      fetch(`/api/users/${self.$route.params.user_id}/follow`,{
        method: "POST",
        headers: {
          "Authorization": `Bearer ${JSON.parse(localStorage.current_user).token}`,
          "Content-Type": "application/json",
          'X-CSRFToken': token
        },
        credentials: 'same-origin',
        body: JSON.stringify({"follower_id": JSON.parse(localStorage.current_user).id, "user_id": self.$route.params.user_id})
      }).then(function(response){
        return response.json();
      }).then(function(jsonResponse){
        
        if(jsonResponse.hasOwnProperty("message") && jsonResponse.status==201 ){
          $("#followclick")[0].innerHTML="Following";
          $("#followclick").removeClass("btn-primary");
          $("#followclick").addClass("btn-success")
          ++ self.user.followers;
        }
        
      }).catch(function(error){
        console.log(error)
      });
    }
  },
  created: function(){
    self = this;
    
    fetch(`/api/users/${self.$route.params.user_id}/posts`,{
      method: "GET",
      headers: {
        "Authorization": `Bearer ${JSON.parse(localStorage.current_user).token}`
      }
    }).then(function(response){
      return response.json();
    }).then(function(jsonResponse){
      self.user = jsonResponse.post_data;
    }).catch(function(error){
      console.log(error);
    });
  },
  data: function(){
    return {
      user: null,
      activeuser: (this.$route.params.user_id == JSON.parse(localStorage.current_user).id) ? true : false
    }
  }
});
   
// Define Routes
const router = new VueRouter({
    routes: [
        { path: "/", component: Home },
        { path: "/register", component: Register},
        { path: "/login", component: Login},
        { path: "/explore", component: Explore},
        { path: "/users/:user_id", name:"users",component: Profile},
        { path: "/posts/new", component: NewPost},
        { path: "/logout", component: Logout}
    ]
});

// Instantiate our main Vue Instance
let app = new Vue({
    el: "#app",
    router
});