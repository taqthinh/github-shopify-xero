import {DataTable, DatePicker, Checkbox ,Select, AppProvider, Card,TextField, Button, TextStyle, EmptyState, Form, FormLayout, Layout, Page } from '@shopify/polaris';
import React, {Component, useState, useCallback} from 'react';
import ReactDOM from "react-dom";
import '@shopify/polaris/dist/styles.css';
import translations from '@shopify/polaris/locales/en.json';
const AppConfig = window.config;
console.log("1111111111: "+ window.config)

function DatePickerExample() {
  const [{month, year}, setDate] = useState({month: new Date().getMonth(), year: new Date().getFullYear()});
  const [selectedDates, setSelectedDates] = useState({
    start: new Date(),
    end: new Date(),
  });
  const handleMonthChange = useCallback(
    (month, year) => setDate({month, year}),
    [],
  );
  return (
    <DatePicker
      month={month}
      year={year}
      onChange={setSelectedDates}
      onMonthChange={handleMonthChange}
      selected={selectedDates}
      multiMonth
      allowRange
    />
  );
}

function ExportForm(){
    return(
        <Form>
            <DatePickerExample />
            <br />
            <Button primary>Export Data</Button>
        </Form>
    )
}

function AutoSyncCheckbox(props) {
    // const label =
  const [checked, setChecked] = useState(false);
  const handleChange = useCallback((newChecked) => setChecked(newChecked), []);

  return (
    <Checkbox
      label= "Auto Sync"
      checked={checked}
      onChange={handleChange}
    />
  );
}

function AccountSelect(props) {

    const [selected, setSelected] = useState(props.current_account);
    console.log(props.current_account)
    console.log(props.accounts)
    const handleSelectChange = useCallback((value) => setSelected(value), []);
    const options = props.accounts.map((account) =>
        {label: account['name']; value: account['code']}
    )
    console.log('OPTIONS: ' + options)

    /* const options = [
    // {label: '200 - Sale', value: '200'},
    // {label: '201 - VAT', value: '201'},
    // {label: '901 - Bank', value: '901'},
    // ]; */

    return (
    <Select
        label= {props.label}
        options={options}
        onChange={handleSelectChange}
        value={selected}
    />
    );
}

function ShippingAccountSelect(props) {
  const [selected, setSelected] = useState('200');

  const handleSelectChange = useCallback((value) => setSelected(value), []);

  const options = [
    {label: '200 - Sale', value: '200'},
    {label: '201 - VAT', value: '201'},
    {label: '901 - Bank', value: '901'},
  ];

  return (
    <Select
      label= {props.label}
      options={options}
      onChange={handleSelectChange}
      value={selected}
    />
  );
}

function PaymentAccountSelect(props) {
  const [selected, setSelected] = useState('200');

  const handleSelectChange = useCallback((value) => setSelected(value), []);

  const options = [
    {label: '200 - Sale', value: '200'},
    {label: '201 - VAT', value: '201'},
    {label: '901 - Bank', value: '901'},
  ];

  return (
    <Select
      label= {props.label}
      options={options}
      onChange={handleSelectChange}
      value={selected}
    />
  );
}

function AccountSettingForm(){
    const sale_accounts = AppConfig.sale_accounts
    const shipping_accounts = AppConfig.shipping_accounts
    const payment_accounts = AppConfig.payment_accounts
    const shopify_store = AppConfig.shopify_store

    return (
        <Form>
            <AutoSyncCheckbox />
            <br />
            <Button primary>Save Settings</Button>
        </Form>
    )
}

function DataTableExample() {
  const rows = [
    ['Emerald Silk Gown', '$875.00', 124689, 140],
    ['Mauve Cashmere Scarf', '$230.00', 124533, 83],
  ];
  return (
    <Page>
      <Card>
        <Card.Section>
        <p>History log of sync history, including automated jobs.</p>
        <p> Orders synced this month: 55 </p>
        <p>Current Orders per plan: 100</p>
        </Card.Section>
        <DataTable
          columnContentTypes={[
            'datetime',
            'datetime',
            'text',
            'text',
          ]}
          headings={[
            'Excution Time',
            'Finish Time',
            'Status',
            'Message',
          ]}
          rows={rows}
        />
      </Card>
    </Page>
  );
}

function DisconnectForm(){
    return(
        <Card >
            <Card.Section>
                <p>Organization Name: </p>
                <p >Status: <span style={{color:'green'}}><b>Connected</b></span></p>
                <Button destructive>Disconnect From Xero</Button>
            </Card.Section>
        </Card>
    )
}

function PlanForm(){
    return(
        <Layout >
            <Layout.Section oneThird>
                <div className="card">
                    <div className="card-body d-flex flex-column">
                        <Card title="Plan name1"
                          sectioned>
                        <p><b>Free</b></p>
                        <p>Sync Customers, Products, Orders to Xero</p>
                        <p>Manually Sync in date range</p>
                        <p>Automatic Updates every 24 hours</p>
                        <p>Account Mapping</p>
                        <p>Synchronization History</p>
                        <p>100 Orders/month</p>
                    </Card>
                    </div>
                </div>
            </Layout.Section>
            <Layout.Section oneThird>
                <div className="card">
                    <div className="card-body d-flex flex-column">
                        <Card title="Plan name2"
                              sectioned>
                            <Form>
                                <p><b>$19.99/month</b></p>
                                <p>All Essential Features</p>
                                <p>Automatic Updates every 12 hours</p>
                                <p>Sync Gift Cards, Refunds to Xero</p>
                                <p>800 Orders/month</p>
                                <div style={{textAlign:'center', marginTop:'10px'}}>
                                    <Button primary>Sign Up</Button>

                                </div>
                            </Form>
                        </Card>
                    </div>
                </div>

            </Layout.Section>
            <Layout.Section oneThird>
                <div className="card">
                    <div className="card-body d-flex flex-column">
                        <Card title="Plan name3"
                        sectioned>
                        <Form>
                            <p><b>$29.99/month</b></p>
                            <p>All Standard Features</p>
                            <p>Automatic Updates every 3 hours</p>
                            <p>Unlimited Orders per month</p>
                            <div style={{textAlign:'center', marginTop:'10px'}}>
                                <Button primary>Sign Up</Button>
                            </div>
                        </Form>
                    </Card>
                    </div>
                </div>
            </Layout.Section>
        </Layout>
    )
}

class Hello extends Component{

    constructor(props) {
        super(props);
        this.state = {
            config: AppConfig,
        }
    }
    render() {
        return (
            <AppProvider i18n={translations}>
                <Page title="General Settings">
                  <Layout>
                    <Layout.AnnotatedSection
                    description={
                        <p>
                          Please choose your account accordingly: <br />
                        - Sales Account will be applied to Invoice Line Items' Account<br />
                        - Shipping Account will be applied to Shipping as an Invoice Line Item<br />
                        - Payments will go to Payment Account on Xero
                        </p>
                    }
                        >
                        <AccountSettingForm />
                    </Layout.AnnotatedSection>
                  </Layout>
                </Page>
                <Page title="Export To Xero">
                  <Layout>
                    <Layout.AnnotatedSection
                    description={
                        <p>
                        - Choose date from and date to and export your data to Xero.<br />
                        - Customers will be synced to Xero as: Shopify - "Customer Name" - ("Customer Id")<br />
                        - Invoices will be synced to Xero as: Shopify - "Order Id"<br />
                        - Products will be synced to Xero as Xero Items
                        </p>
                    }>
                        <ExportForm />
                    </Layout.AnnotatedSection>
                      </Layout>
                </Page>
                <Page title="History">
                  <Layout>
                      <Layout.Section>
                        <DataTableExample />
                    </Layout.Section>
                  </Layout>
                </Page>
                <Page title="Plans">
                    <PlanForm />
                </Page>
                <Page title="Disconnect From Xero">
                    <DisconnectForm />
                </Page>

            </AppProvider>
        )
    }

}

export default Hello;

const wrapper = document.getElementById("container12");
wrapper ? ReactDOM.render(<Hello />, wrapper) : false;





