import React from 'react';
import './Home.css';
import second from './second.png'

var fileDownload = require('js-file-download')

class Home extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      file: '',
      type: 'file',
      json: null,
      text: null,
    }
    this.onchange = this.onchange.bind(this);
    this.authenticate = this.authenticate.bind(this);
    this.check = this.check.bind(this);
    this.getCookie = this.getCookie.bind(this);
    this.load_srt = this.load_srt.bind(this);
    this.load_text = this.load_text.bind(this);
    this.load_json = this.load_json.bind(this);
    this.copy_json = this.copy_json.bind(this);
    this.copy_text = this.copy_text.bind(this);
    this.call_data = this.call_data.bind(this);
  }

  getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        // Does this cookie string begin with the name we want?
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

  async onchange(e) {
    const file = e.target.files[0]
    this.setState({ file: file });
    this.setState({ type: 'submit' })
  }

  async authenticate() {
    this.setState({ type: '' })
    let formdata = new FormData();
    formdata.append('file', this.state.file);
    var csrftoken = this.getCookie('csrftoken');
    var headers = new Headers();
    headers.append('X-CSRFToken', csrftoken);
    const fetchResponse = await fetch('pass', {
      method: 'post',
      headers: headers,
      body: formdata,
    });
    this.setState({ type: 'check' })
    await fetchResponse.json().then(data => {
    });
  }

  async call_data() {
    var csrftoken = this.getCookie('csrftoken');
    var headers = new Headers();
    headers.append('X-CSRFToken', csrftoken);
    const fetchResponse = await fetch('data_text', {
      method: 'post',
      headers: headers
    });
    await fetchResponse.json().then(data => {

      this.setState({ json: data });
      let ans = '';
      for (let i = 0; i < data['messages'].length; i++) {
        ans += data['messages'][i]['text'];
        ans += "\n";
      }
      this.setState({ text: ans })
    });
  }

  async load_srt() {
    var csrftoken = this.getCookie('csrftoken');
    var headers = new Headers();
    headers.append('X-CSRFToken', csrftoken);
    const fetchResponse = await fetch('data_srt', {
      method: 'post',
      headers: headers
    });
    await fetchResponse.json().then(data => {
      fileDownload(data['transcript']['payload'], 'filename.text');
    });
  }

  async load_text() {
    fileDownload(this.state.text, 'filename.text');
  }

  async load_json() {
    const jsonString = `data:text/json;chatset=utf-8,${encodeURIComponent(
      JSON.stringify(this.state.json)
    )}`;
    const link = document.createElement("a");
    link.href = jsonString;
    link.download = "data.json";

    link.click();
  }

  async copy_json() {
    navigator.clipboard.writeText(JSON.stringify(this.state.json))
  }

  async copy_text() {
    navigator.clipboard.writeText(this.state.text)
  }

  async check() {
    var csrftoken = this.getCookie('csrftoken');
    var headers = new Headers();
    headers.append('X-CSRFToken', csrftoken);
    const fetchResponse = await fetch('check', {
      method: 'post',
      headers: headers
    });
    await fetchResponse.json().then(data => {
      if (data['status'] == 'completed') {
        this.setState({ type: 'load' });
        this.call_data();
      }
    });
  }

  render() {
    return (
      <div>
        <div>
          <p id="top">
            Transcript
          </p>
        </div>
        <div>
          <img src={second} alt="My image" />
        </div>
        <div id="parallel">
          <div>
            <h1>
              Convert any Video File to Text.
            </h1>
            <br />
            <h2>
              Download in different Formats
            </h2>
            <br />
            <h3>
              Srt&nbsp;&nbsp;Json&nbsp;&nbsp;Text
            </h3>
            <br />
            <br />
            <h1>
              {this.state.type == 'check' ? "Status : In Progress" : this.state.type == 'load' ? "Status : Completed" : null}
            </h1>
            <br />
            <h3>
              Please dont't refresh the page
            </h3>
          </div>
          <div>
            {this.state.type == 'submit' || this.state.type == 'check' ? <button onClick={this.state.type == 'submit' ? this.authenticate : this.check} className='button-27'>{this.state.type}</button> : this.state.type == 'file' ? <input name='file' onChange={this.onchange} className="button-27" type="file" /> : null}
            <br />
            <br />
            {this.state.type == 'load' ? <button onClick={this.load_srt} className='button-27'>Download Subtitles</button> : null}
            <br />
            <br />
            {this.state.type == 'load' ? <button onClick={this.load_text} className='button-27'>Download Text</button> : null}
            <br />
            <br />
            {this.state.type == 'load' ? <button onClick={this.load_json} className='button-27'>Download Json</button> : null}
          </div>
        </div>
        <div id='parallel'>
          {this.state.type == 'load' ? <div><button onClick={this.copy_text} className='button-27'>Copy Text</button>
            <br />
            <br />
            <button onClick={this.copy_json} className='button-27'>Copy Json</button></div> : null}
        </div>
        <div id="footer">
          Footer
        </div>
      </div>
    )
  }
}

export default Home;
