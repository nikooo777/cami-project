/*eslint-disable react/prop-types*/

import React from 'react';
import CounterViewContainer from './counter/CounterViewContainer';
import ColorViewContainer from './colors/ColorViewContainer';
import HomepageViewContainer from './homepage/HomepageViewContainer';
import HomepageViewContainerCaregiver from './homepage-caregiver/HomepageViewContainer';
import JournalViewContainer from './journal/JournalViewContainer';

/**
 * AppRouter is responsible for mapping a navigator scene to a view
 */
export default function AppRouter(props) {
  const key = props.scene.route.key;
  switch (key) {
    case 'HomepageCaregiver':
      return <HomepageViewContainerCaregiver />;
    case 'Counter':
      return <CounterViewContainer />;
    case 'Journal':
      return <JournalViewContainer />;
    case 'Homepage':
      return <HomepageViewContainer />;
    default:
      throw new Error('Unknown navigation key: ' + key);
  }
}