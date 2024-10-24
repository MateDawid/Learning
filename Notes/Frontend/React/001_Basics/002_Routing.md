# Routing

> Source: https://testdriven.io/courses/taxi-react/react-routing/

React does not include a native client-side routing library. Luckily, the React developer community provides many open source routing solutions. React Router, the one we'll be using in this tutorial, is by far the most popular React routing library.

Let's get started by installing the appropriate package from yarn. Enter the following command into your terminal.

```
$ yarn add react-router-dom@6.4.3
```

The simplest client-side routing configuration requires a Router, a Routes, and a Route:

1. A Router maintains a specialized history object as you navigate between different views.
2. A Routes is the base component that holds the tree of Routes.
3. A Route matches a URL and loads a component onto the screen.

React Router recommends using the HashRouter for web applications that use a static file server. Recall that we're using Django to serve API endpoints not templates, so HashRouter is exactly what we want. All HashRouter URLs will begin with #/ followed by a path.

Since we intend to use routing throughout our entire application, let's add our Routes and Routes components directly to the index.js file:

```javascript
// client/src/index.js

import React from 'react';
import ReactDOM from 'react-dom';
import { HashRouter, Route, Routes } from 'react-router-dom'; // new
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';

// changed
ReactDOM.render(
  <React.StrictMode>
    <HashRouter>
      <Routes>
        <Route path='/' element={<App />} />
      </Routes>
    </HashRouter>
  </React.StrictMode>,
  document.getElementById('root')
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
```

With basic routing implemented, let's add a few more component views to give our app life. Make a new "client/src/components/" directory and then create three JavaScript files -- SignUp.js, LogIn.js, and Landing.js -- inside it.

```
# From the client directory
$ mkdir -p src/components
$ touch src/components/{SignUp,LogIn,Landing}.js
```

The SignUp component should include a link back to the home (landing) page and a link to the log in page. A <Link> is React Router's equivalent of an HTML `<a>` element. We'll use the to attribute in the same way an href is used in an anchor tag.

```javascript
// client/components/SignUp.js

import React from 'react';
import { Link } from 'react-router-dom';

function SignUp (props) {
  return (
    <>
      <Link to='/'>Home</Link>
      <h1>Sign up</h1>
      <p>
        Already have an account? <Link to='/log-in'>Log in!</Link>
      </p>
    </>
  );
}

export default SignUp;
```

> **React Fragments**
> 
> Are you wondering what <> and `` mean? Those are short syntax forms of React Fragments. Fragments let you group child elements without needing to add extra nodes to the DOM.

The LogIn component should look almost identical to the SignUp component with a link back home and a link to the sign up page.

```javascript
// client/src/components/LogIn.js

import React from 'react';
import { Link } from 'react-router-dom';

function LogIn (props) {
  return (
    <>
      <Link to='/'>Home</Link>
      <h1>Log in</h1>
      <p>
        Don't have an account? <Link to='/sign-up'>Sign up!</Link>
      </p>
    </>
  );
}

export default LogIn;
```

Add the following code to Landing.js:

```javascript
// client/src/components/Landing.js

import React from 'react';
import { Link } from 'react-router-dom';

function Landing (props) {
  return (
    <div>
      <h1>Taxi</h1>
      <Link to='/sign-up'>Sign up</Link>
      <Link to='/log-in'>Log in</Link>
    </div>
  );
}

export default Landing;
```

Before we can test our application again, we need to add top-level routes for our new components. Open index.js again and add the following code.

```javascript
// client/src/index.js

import React from 'react';
import ReactDOM from 'react-dom';
import { HashRouter, Route, Routes } from 'react-router-dom';
import './index.css';
import App from './App';
// new begin
import Landing from './components/Landing';
import LogIn from './components/LogIn';
import SignUp from './components/SignUp';
// new end
import reportWebVitals from './reportWebVitals';

ReactDOM.render(
  <React.StrictMode>
    <HashRouter>
      <Routes>
        <Route path='/' element={<App />} />
        {/* new begin */}
        <Route index element={<Landing />} />
        <Route path='sign-up' element={<SignUp />} />
        <Route path='log-in' element={<LogIn />} />
        {/* new end */}
      </Routes>
    </HashRouter>
  </React.StrictMode>,
  document.getElementById('root')
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
```

Note how we are using the `index` attribute on the `Route` component that renders `Landing`. Index routes are "default children". In the case of our application, whenever the root is visited, the UI will render the Landing component.

Then, change the code in App.js like so:

```javascript
// client/src/App.js

import React from 'react';
import { Outlet } from 'react-router-dom'; // changed

import './App.css';

// changed
function App () {
  return (
    <>
      <Outlet />
    </>
  );
}

export default App;
```

Note that we are replacing the contents with an Outlet component. This is where all of the nested Routes will be rendered.

Refresh the browser and click around the app. You should be able to navigate between the home, sign up, and log in pages.
