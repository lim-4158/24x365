// MainPage.js
import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Tab, Tabs, TabList, TabPanel } from 'react-tabs';
import 'react-tabs/style/react-tabs.css';
import ChatComponent from './ChatComponent';
import GoogleSignInButton from './GoogleSignInButton';
import UserCalendar from './UserCalendar';
import EventChecklist from './EventChecklist';
import './MainPage.css';

const MainPage = () => {
  const navigate = useNavigate();
  const [selectedTab, setSelectedTab] = useState(0);

  // Function to check if the user is authenticated
  const isAuthenticated = () => {
    const token = localStorage.getItem('token');
    return token !== null;
  };

  useEffect(() => {
    if (!isAuthenticated()) {
      navigate('/login'); // Redirect to login page if not authenticated
    } else {
      const savedTabIndex = localStorage.getItem('selectedTabIndex');
      if (savedTabIndex !== null) {
        setSelectedTab(parseInt(savedTabIndex, 10));
      }
    }
  }, [navigate]);

  const handleSelect = (index) => {
    setSelectedTab(index);
    localStorage.setItem('selectedTabIndex', index);
  };

  return (
    <div className="main-page-container">
      <div className="tabs-container">
        <Tabs selectedIndex={selectedTab} onSelect={handleSelect}>
          <TabList>
            <Tab>ChatBot</Tab>
            <Tab>User Calendar</Tab>
            <Tab>Event Checklist</Tab>
            <Tab>Reconnect with Google</Tab>
          </TabList>

          <TabPanel>
            <ChatComponent />
          </TabPanel>
          <TabPanel>
            <UserCalendar />
          </TabPanel>
          <TabPanel>
            <EventChecklist />
          </TabPanel>
          <TabPanel>
            <GoogleSignInButton />
          </TabPanel>
        </Tabs>
      </div>
    </div>
  );
};

export default MainPage;
