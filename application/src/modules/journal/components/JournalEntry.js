import React, {PropTypes} from 'react';
import {
  StyleSheet,
  Text,
  View
} from 'react-native';

import moment from 'moment';
import Icon from 'react-native-vector-icons/FontAwesome';
import icons from 'Cami/src/icons-fa';
import variables from '../../variables/CaregiverGlobalVariables';

const styles = StyleSheet.create({
  journalEntry: {
    backgroundColor: 'white',
    marginBottom: 20,
    flexDirection: 'row',
    justifyContent: 'flex-start',
    alignItems: 'center'
  },
  iconContainer: {
    width: 80,
    paddingTop: 20,
    paddingLeft: 20,
    paddingRight: 20,
    paddingBottom: 20,
    flexDirection: 'column',
    alignSelf: 'flex-start',
    alignItems: 'center',
    zIndex: 7
  },
  icon: {
    alignItems: 'center'
  },
  statusIcon: {
    position: 'absolute',
    width: 16,
    height: 16,
    top: -8,
    left: 73,
    justifyContent: 'center',
    alignItems: 'center',
    zIndex: 8,
    borderRadius: 8
  },
  time: {
    fontSize: 12,
    fontWeight: 'bold',
    paddingTop: 10,
    color: variables.colors.gray.neutral
  },
  textContainer: {
    flex: 1,
    flexWrap: 'wrap',
    justifyContent: 'center',
    flexDirection: 'column',
    paddingTop: 20,
    paddingBottom: 20,
    marginRight: 20,
    marginLeft: 20
  },
  text: {
    flex: 1,
    fontSize: 12,
  },
  statusMessage: {
    color: variables.colors.gray.dark
  },
  actionMessage: {
    paddingTop: 10,
    marginTop: 10,
    borderTopWidth: 1,
    borderStyle: 'solid',
    borderTopColor: variables.colors.gray.light
  },
});

const JournalEntry = React.createClass({
  propTypes: {
    type: PropTypes.string.isRequired,
    status: PropTypes.string.isRequired,
    timestamp: PropTypes.number.isRequired,
    title: PropTypes.string.isRequired,
    message: PropTypes.string.isRequired
  },

  matchStatus() {
    var status = this.props.status;

    if (status !== 'none') {
      return status;
    } else {
      // this will be the case for activity-related entries
      switch (this.props.type) {
        case 'exercise': return 'info';
        case 'medication': return 'info';
        case 'appointment': return 'info';
        default: return 'info';
      }
    }
  },

  render() {
    const time = moment(new Date(this.props.timestamp * 1000)).format('HH:mm');

    return (
      <View style={styles.journalEntry}>
        <View style={styles.iconContainer}>
          <View style={styles.icon}>
            <Icon name={icons[this.props.type]} size={30} color={variables.colors.status[this.matchStatus()]}/>
          </View>
          <View>
            <Text style={styles.time}>{time}</Text>
          </View>
          <View style={[styles.statusIcon, {backgroundColor: variables.colors.status[this.matchStatus()]}]}>
            <Icon name={icons[this.matchStatus()]} size={12} color={'white'}/>
          </View>
        </View>
        <View style={{flex: 7, borderLeftWidth: 2, borderColor: variables.colors.status[this.matchStatus()]}}>
          <View style={[styles.textContainer]}>
            <View style={{flexWrap: 'wrap'}}>
              <Text style={[styles.text, {color: variables.colors.gray.darker}]}>{this.props.title}</Text>
            </View>
            {
              this.props.message
                ? <View style={[styles.actionMessage, {flexWrap: 'wrap'}]}>
                    <Text style={[styles.text, {color: variables.colors.gray.dark}]}>{this.props.message}</Text>
                  </View>
                : false
            }
          </View>
        </View>
      </View>
    );
  }
});

export default JournalEntry;
