import React from 'react';
import { Tab, Tabs, TabList, TabPanel } from 'react-tabs';
import 'react-tabs/style/react-tabs.css';
import ChatComponent from './ChatComponent';
import GoogleSignInButton from './GoogleSignInButton';
import UserCalendar from './UserCalendar';

const MainPage = () => {
  return (
    <div className="main-page-container">
      <Tabs>
        <TabList>
          <Tab>ChatBot</Tab>
          <Tab>Google Sign-In</Tab>
          <Tab>User Calendar</Tab>
        </TabList>

        <TabPanel>
          <ChatComponent />
        </TabPanel>
        <TabPanel>
          <GoogleSignInButton />
        </TabPanel>
        <TabPanel>
          <UserCalendar />
        </TabPanel>
      </Tabs>
    </div>
  );
};

export default MainPage;
