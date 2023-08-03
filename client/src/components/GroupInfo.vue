<template>
    <div class="group-info">
      <h5 class="card-title">{{ name }} ({{ groupId }})</h5>
      <ul class="list-unstyled">
        <li v-for="member in members" :key="member" class="small">{{ member }}</li>
      </ul>
      <div class="image-container">
        <div v-show="handRaised" class="image-wrapper">
          <div @click="handOff">
            <img src="../assets/handup.png" alt="Hand Raised" class="image" />
          </div>
        </div>
        <div v-show="atCheckpoint" class="image-wrapper">
          <div @click="checkOff">
            <img src="../assets/check.png" alt="At Checkpoint" class="image" />
          </div>
        </div>
      </div>
      <div class="progress" style="height: 30px;">
        <div class="progress-bar bg-success" role="progressbar" :style="{width: progressPercent + '%'}" aria-valuenow="{{progress}}" aria-valuemin="0" aria-valuemax="100"></div>
          <div class="justify-content-center d-flex position-absolute w-100">
            <p class="progress-text">
              <b>{{ progress }}/{{ maxProgress }}</b>
            </p>
          </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'GroupInfo',
    props: {
      name: { type: String },
      members: { type: Array },
      maxProgress: { type: Number, default: 0 },
      groupId: { type: Number },
      score: { type: Number },
      handRaised: { type: Boolean },
      atCheckpoint: { type: Boolean },
      progress: { type: Number }
    },
    computed: {
      progressPercent() {
        return (this.progress/this.maxProgress) * 100
      }
    },
    methods: {
      checkOff() {
        this.$emit('instructorCommand', 'checkoff', this.name);
      },
      handOff() {
        this.$emit('instructorCommand', 'handoff', this.name);
      }
    }
  }
  </script>
  
  <style scoped>
  .group-info {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    height: 100%;
  }
  
  .card-title {
    color: #333333;
    font-size: 1.2rem;
    margin-bottom: 10px;
  }
  
  ul.list-unstyled {
    margin-bottom: 10px;
  }
  
  .small {
    font-size: 0.8rem;
  }
  
  .image-container {
    display: flex;
    justify-content: center;
    align-items: center;
  }
  
  .image-wrapper {
    margin-right: 10px;
  }
  
  .image {
    width: 96px;
    height: 96px;
  }
  
  .progress-text {
    margin-top: auto;
    margin-bottom: 5px;
    font-size: 1.2rem;
  }
  
  .card-title,
  .small {
    color: #555555;
  }
  </style>
  