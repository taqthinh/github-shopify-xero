import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';

function ThienanBlog() {
  return (
    <div>Thienanblog xin chào các bạn độc giả</div>
  );
}

function Abc() {
    return (
        <h1>Method must Upcase</h1>
 );
}

class App extends Component {
  render() {
    return (
      <div className="App">
        <div className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <h2>Welcome to React</h2>
        </div>
        <p className="App-intro">
            <Abc />
            <ThienanBlog />
        </p>
      </div>
    );
  }
}

export default App;
