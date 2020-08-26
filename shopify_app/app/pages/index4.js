import {AppProvider, Button, Card,TextField, TextStyle, EmptyState, Form, FormLayout, Layout, Page } from '@shopify/polaris';
import React, {Component, useState, useCallback} from 'react';
import ReactDOM from "react-dom";
import '@shopify/polaris/dist/styles.css';
import translations from '@shopify/polaris/locales/en.json';


class SettingButton extends Component{
    render(){
        return(
            <Form >
                <Button submit>Setting</Button>
            </Form>
        )
    }
}

class NameForm extends Component{

    constructor(props) {
        super(props);
        this.state = {name: ''};
        this.handleNameChange = this.handleNameChange.bind(this)
        this.handleSubmit = this.handleSubmit.bind(this)
    }

    handleNameChange(event){
        this.setState({name: event.target.value});
    }

    handleSubmit(event){
        alert("Name: " + this.state.name)
        event.preventDefault();
    }

    render(){
        return(
            <Form onSubmit={this.handleSubmit}>
                <FormLayout>
                    <TextField
                    value={this.state.name}
                    onChange={this.handleNameChange}
                    label="Name"
                    helpText={<span>Polaris</span>}
                    />
                    <Button submit>Submit</Button>
                </FormLayout>
            </Form>
        )
    }
}

function NameFormExample(){
    const [name, setName] = useState('');

    const handleSubmit = useCallback((_event) => {
    alert(" Name: "+ name)
    }, [name]);

    const handleNameChange = useCallback((value) => setName(value), []);

    return (
    <Form onSubmit={handleSubmit}>
      <FormLayout>
        <TextField
          value={name}
          onChange={handleNameChange}
          label="Name"
          type="text"
          helpText={
            <span>
              Polaris
            </span>
          }
        />

        <Button submit>Submit</Button>
      </FormLayout>
    </Form>
  );

}



class Hello extends Component {

    constructor(props){
        super(props);
        this.state = {
            message:'Welcome to code 101'
        };
    }

    render() {
        return (
            <AppProvider i18n={translations}>
                <Page>
                    <Layout>
                        <Layout.Section oneThird>
                            <SettingButton />
                        </Layout.Section>
                        <Layout.Section oneThird>
                            <Card title="General Settings" sectioned>
                              <NameFormExample />
                            </Card>
                            <Card title="Export To Xero" sectioned>
                              <NameFormExample />
                            </Card>
                            <Card title="History" sectioned>
                              <NameFormExample />
                            </Card>
                            <Card title="Plans" sectioned>
                              <NameFormExample />
                            </Card>
                            <Card title="Disconnect From Xero" sectioned>
                              <NameFormExample />
                            </Card>
                        </Layout.Section>

                    </Layout>
                </Page>
            </AppProvider>
        )
    }

}

const Index = () => (
    <Hello />
);

export default Hello;

// const wrapper = document.getElementById("container12");
// wrapper ? ReactDOM.render(<Hello />, wrapper) : false;





