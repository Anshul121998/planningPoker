<template>
  <div class="JoinRoom">
    <br />
    <v-snackbar v-model="snackbar" :color="alertColor" timeout="6000" top right>
      {{ alertText }}
      <template v-slot:action="{ attrs }">
        <v-btn dark text v-bind="attrs" @click="snackbar = false">Close</v-btn>
      </template>
    </v-snackbar>
    <v-overlay :value="isLoading" opacity="0.20">
      <v-progress-circular
        :size="100"
        :width="7"
        color="indigo"
        indeterminate
      ></v-progress-circular>
    </v-overlay>
    <v-container class="fill-height" fluid>
      <v-row align="center" justify="center">
        <v-col cols="12" sm="8" md="4">
          <v-card class="elevation-12">
            <v-toolbar color="primary" class="elevation-6" dark flat>
              <v-toolbar-title>JOIN ROOM</v-toolbar-title>
            </v-toolbar>
            <v-card-text>
              <v-form>
                <v-text-field
                  label="Room ID"
                  name="roomID"
                  prepend-icon="mdi-numeric"
                  type="text"
                  v-model="roomId"
                  :rules="[() => !!roomId || 'this field is required']"
                  required
                ></v-text-field>
                <v-text-field
                  label="Participant Name"
                  name="pName"
                  prepend-icon="mdi-account"
                  type="text"
                  v-model="pName"
                  :rules="[() => !!pName || 'this field is required']"
                  required
                ></v-text-field>
                <v-select
                  label="Estimate"
                  :items="estimateItems"
                  prepend-icon="mdi-help-circle-outline"
                  v-model="eItem"
                  @change="getEstimation(eItem)"
                  :rules="[() => !!pName || 'this field is required']"
                  required
                ></v-select>
              </v-form>
            </v-card-text>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="primary" :disabled="allOkay" @click="sendParticipantData()" class="mb-2 ml-12">Send</v-btn>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>
      <v-row align="center" justify="center">
        <h3>{{ estimateHelp }}</h3>
      </v-row>
    </v-container>
  </div>
</template>

<script>
import JoinRoomService from '@/services/JoinRoomService.js'
export default {
  name: 'JoinRoom',
  watch: {
    pName: function (val) {
      if (val !== '' && this.eItem !== '' && this.roomId !== '') {
        this.allOkay = false
      } else {
        this.allOkay = true
      }
    },
    roomId: function (val) {
      if (val !== '' && this.eItem !== '' && this.pName !== '') {
        this.allOkay = false
      } else {
        this.allOkay = true
      }
    },
    eItem: function (val) {
      if (val !== '' && this.pName !== '' && this.roomId !== '') {
        this.allOkay = false
      } else {
        this.allOkay = true
      }
    }
  },
  data: () => ({
    estimateItems: [
      '0',
      '0.5',
      '1',
      '2',
      '3',
      '5',
      '8',
      '13',
      '21',
      'Infinity'
    ],
    estimateExplaination: {
      '0': 'Meaning: This does not qualify as a user story for us, please check.',
      '1': 'Meaning: Almost no effort, can be done in a matter of few hours.',
      '2': 'Meaning: Path to solve the problem is clear, can be completed by 1/8th of sprint.',
      '3': 'Meaning: Path to solve the problem is clear, can be completed by quarter of the sprint.',
      '5': 'Meaning: Path to solve the problem is clear, can be completed by mid sprint.',
      '8': 'Meaning: Path to solve the problem is not clear, quite complex. Worst case, might end up consuming whole sprint.',
      '13': 'Meaning: Path to solve the problem is unknown. Hard to complete during a sprint, might spill over. Try breaking this into smaller User stories and indentify blockers.',
      '21': 'Meaning: Problem too big, need to break this one to proceed.',
      'Infinity': 'Meaning: No idea, please explain again...'
    },
    isLoading: false,
    estimateHelp: '',
    roomId: '',
    eItem: '',
    pName: '',
    alertColor: 'info',
    snackbar: false,
    alertText: '',
    allOkay: true
  }),
  methods: {
    getEstimation (item) {
      this.estimateHelp = this.estimateExplaination[item]
    },
    sendParticipantData () {
      var data = {}
      data['uuid'] = this.roomId
      data['name'] = this.pName
      data['estimate'] = String(this.eItem)
      this.isLoading = true
      var self = this
      JoinRoomService.enterRoom(data).then(
        (response) => {
          if (response < 0) {
            self.alertColor = 'error'
            self.alertText = 'Room ID does not exist!'
          } else if (response > 0) {
            self.alertColor = 'success'
            self.alertText = 'Estimate successfully saved.'
          } else {
            self.alertColor = 'info'
            self.alertText = 'Currently room is not accepting estimates.'
          }
          self.snackbar = true
          self.isLoading = false
        },
        () => {
          self.alertColor = 'error'
          self.alertText = 'Error occurred, reload Page!'
          self.snackbar = true
          self.isLoading = false
        }
      )
    }
  }
}
</script>

<style lang="scss" scoped>
.JoinRoom {
  padding-left: 0.5rem;
  padding-right: 0.5rem;
}
</style>
