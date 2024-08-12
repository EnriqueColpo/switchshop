<script setup lang="ts">
import { SplitterGroup, SplitterPanel, SplitterResizeHandle } from 'radix-vue'
import './style.css'

</script>

<template>
  <div class="flex w-full pt-1 content-start justify-center">
      <div class="w-9/12 content-start">
          <SplitterGroup
            id="splitter-group-1"
            direction="horizontal"
          >

            <SplitterPanel
              id="splitter-group-1-panel-1"
              :min-size="30"
              class="SplitterPanel p-1"
            >
              <slot name="content" />

            </SplitterPanel>

            <SplitterResizeHandle
              id="splitter-group-1-resize-handle-1"
              class="SplitterResizeHandle"
            />
          </SplitterGroup>
    </div>

  </div>
</template>